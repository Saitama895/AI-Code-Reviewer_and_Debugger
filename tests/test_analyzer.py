import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pydantic import ValidationError

from code_reviewer.analyser import analyze_python

def test_valid_python():
    result = analyze_python("x = 10")

    assert result.status == "success"
    assert result.findings == []
    assert result.errors == []
