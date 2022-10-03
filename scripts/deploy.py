from ape import accounts, project

def main():
    acct = accounts.load("deployer_account")
    eth_pool_contract = project.eth_pool.deploy(0, sender=acct, publish=True)
    erc20_pool_contract = project.erc20_pool.deploy("0x0000000000000000000000000000000000000000", 0, sender=acct, publish=True)
    factory_contract = project.factory.deploy(acct.address, eth_pool_contract.address, erc20_pool_contract.address, sender=acct, publish=True)
    # erc20_pool = acct.deploy(project.erc20_pool, "0x0000000000000000000000000000000000000000", 0)
    # eth_pool = acct.deploy(project.eth_pool, 0)
    # factory = acct.deploy(project.factory, acct.address, eth_pool.address, erc20_pool.address)
    