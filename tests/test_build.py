import unittest
import os
import pytest
import yaml

from swing.core import SwingCore
from swing.helpers import remove_file, remove_directory, is_readable_file, is_readable_dir
from swing.errors import SwingCoreError
from swing.parsers import parse_requirements
from helpers import get_fixtures_path


class ChartBuildTestCase(unittest.TestCase):
    core = None
    session = None
    chart_path = None
    output_path = None
    install_path = None

    @classmethod
    def setUpClass(cls):
        cls.core = SwingCore(api=None)
        cls.chart_path = os.path.join(get_fixtures_path(), 'demo')
        cls.output_path = os.path.join(cls.chart_path, 'docker-stack.yaml')
        cls.install_path = os.path.join(cls.chart_path, 'charts')

    def test_a_build_no_requirements(self):
        with pytest.raises(SwingCoreError):
            self.core.build_chart(self.chart_path, self.output_path)
            
    def test_b_install_requirements(self):
        requirements = parse_requirements(os.path.join(self.chart_path, 'requirements.yaml'))
        
        assert len(requirements) == 2
        assert requirements[0].chart_name == 'redis'
        assert requirements[1].chart_name == 'psql'
        assert requirements[1].file is not None
        
        self.core.install_requirements(requirements, self.install_path)
        files = os.listdir(self.install_path)
        
        assert len(files) == 2
        assert 'redis-1.0.0.zip' in files
        assert 'psql-1.0.0.zip' in files
        
    def test_c_build_chart(self):
        self.core.build_chart(self.chart_path, self.output_path)
        
        assert is_readable_file(self.output_path)
        
        with open(self.output_path, 'r') as f:
            compose = yaml.safe_load(f)
        
        assert compose['services']['postgres'] is not None
        assert compose['services']['redis'] is not None
        assert compose['services']['redis']['command'] == 'redis-server --requirepass password234'
        assert compose['services']['postgres']['environment']['POSTGRES_USER'] == 'root'
        assert compose['services']['postgres']['environment']['POSTGRES_PASSWORD'] == 'secret432'
    
    def test_d_clean_junk(self):
        assert not is_readable_dir(os.path.join(self.chart_path, 'build'))
        assert not is_readable_dir(os.path.join(self.install_path, 'redis-1.0.0'))
        assert not is_readable_dir(os.path.join(self.install_path, 'psql-1.0.0'))

    @classmethod
    def tearDownClass(cls):
        remove_file(cls.output_path)
        remove_directory(cls.install_path)

