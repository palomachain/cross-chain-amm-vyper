import pytest
from typing import Union


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def governance(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def Compass_EVM(accounts):
    return accounts[2]


@pytest.fixture(scope="session")
def alice(accounts):
    return accounts[3]


@pytest.fixture(scope="session")
def ERC20(project, alice):
    return alice.deploy(project.erc20, "Test Token", "TT", 18, 10**6 * 10**18)


@pytest.fixture(scope="session")
def Factory(owner, Compass_EVM, governance, project):
    bytecode = project.eth_pool.contract_type.deployment_bytecode.bytecode
    initcode = get_blueprint_initcode(bytecode)
    tx = project.provider.network.ecosystem.create_transaction(
        chain_id=project.provider.chain_id,
        data=initcode,
        gas_price=project.provider.gas_price,
        nonce=owner.nonce,
    )
    tx.gas_limit = project.provider.estimate_gas_cost(tx)
    tx.signature = owner.sign_transaction(tx)
    receipt = project.provider.send_transaction(tx)
    eth_pool_blueprint = receipt.contract_address

    bytecode = project.erc20_pool.contract_type.deployment_bytecode.bytecode
    initcode = get_blueprint_initcode(bytecode)
    tx = project.provider.network.ecosystem.create_transaction(
        chain_id=project.provider.chain_id,
        data=initcode,
        gas_price=project.provider.gas_price,
        nonce=owner.nonce,
    )
    tx.gas_limit = project.provider.estimate_gas_cost(tx)
    tx.signature = owner.sign_transaction(tx)
    receipt = project.provider.send_transaction(tx)
    erc20_pool_blueprint = receipt.contract_address
    return owner.deploy(project.factory, Compass_EVM, eth_pool_blueprint, erc20_pool_blueprint, governance)


def get_blueprint_initcode(initcode: Union[str, bytes]):
    if isinstance(initcode, str):
        initcode = bytes.fromhex(initcode[2:])
    initcode = b"\xfe\x71\x00" + initcode  # eip-5202 preamble version 0
    initcode = (
        b"\x61" + len(initcode).to_bytes(2, "big") +
        b"\x3d\x81\x60\x0a\x3d\x39\xf3" + initcode
    )
    return initcode
