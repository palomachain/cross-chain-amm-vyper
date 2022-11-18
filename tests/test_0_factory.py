def test_deploy(Factory, Compass_EVM):
    assert Factory.admin() == Compass_EVM
