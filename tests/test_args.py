from testpy.args import parse_args
import pytest

def test_default_args(monkeypatch):
    
    # running with no argument
    monkeypatch.setattr(
        "sys.argv",
        ["testpy"]
    )
    args = parse_args()
    
    assert args.no_cli is False
    assert args.run_all is False
    assert args.run_failed is False
    assert args.discover is False
    assert args.config is None
    # not working
    # assert isinstance(args.VERSION, str)
    

def test_no_cli_flag(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["testpy", "--no-cli"]
    )
    args = parse_args()
    assert args.no_cli is True


def test_config_path(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["testpy", "--config", "config.toml"]
    )

    args = parse_args()
    assert args.config == "config.toml"
    

def test_multiple_flags(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "testpy",
            "--run-all",
            "--discover",
            "--no-cli"
        ]
    )

    args = parse_args()

    assert args.run_all is True
    assert args.discover is True
    assert args.no_cli is True
    
    
def test_invalid_argument(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["testpy", "--banana"]
    )

    with pytest.raises(SystemExit):
        parse_args()
        

def test_version_flag(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["testpy", "--version"]
    )

    with pytest.raises(SystemExit):
        parse_args()

    captured = capsys.readouterr()

    assert "testpy" in captured.out