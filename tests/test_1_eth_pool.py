def test_add_liquidity(Factory, Compass_EVM, project, alice):
    pool_id = 0
    token = "0x0000000000000000000000000000000000000000"
    amount = 10 ** 16
    recipient = "recipient"
    Factory.create_pool(token, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, token)
    pool = project.eth_pool.at(pool_address)
    tx = pool.add_liquidity(amount, recipient, sender=alice, value=amount)
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].pool_id == pool_id
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].token == token
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].amount == amount
    assert list(tx.decode_logs(Factory.AddLiquidity))[
        0].depositor == alice.address
    assert list(tx.decode_logs(Factory.AddLiquidity))[0].recipient == recipient


def test_remove_liquidity(Factory, Compass_EVM, project, alice):
    pool_id = 0
    token = "0x0000000000000000000000000000000000000000"
    amount0 = 10 ** 16
    amount1 = 10 ** 15
    recipient = "recipient"
    Factory.create_pool(token, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, token)
    pool = project.eth_pool.at(pool_address)
    pool.add_liquidity(amount0, recipient, sender=alice, value=amount0)
    init_bal = alice.balance
    Factory.remove_liquidity(pool_id, token, amount1,
                             alice.address, sender=Compass_EVM)
    assert alice.balance == init_bal + amount1


def test_swap_in(Factory, Compass_EVM, project, alice):
    pool_id = 0
    token = "0x0000000000000000000000000000000000000000"
    amount = 10 ** 16
    recipient = "recipient"
    Factory.create_pool(token, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, token)
    pool = project.eth_pool.at(pool_address)
    tx = pool.swap_in(amount, recipient, sender=alice, value=amount)
    assert list(tx.decode_logs(Factory.SwapIn))[0].pool_id == pool_id
    assert list(tx.decode_logs(Factory.SwapIn))[0].token == token
    assert list(tx.decode_logs(Factory.SwapIn))[0].amount == amount
    assert list(tx.decode_logs(Factory.SwapIn))[0].recipient == recipient


def test_swap_out(Factory, Compass_EVM, project, alice):
    pool_id = 0
    token = "0x0000000000000000000000000000000000000000"
    amount0 = 10 ** 16
    amount1 = 10 ** 15
    recipient = "recipient"
    Factory.create_pool(token, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, token)
    pool = project.eth_pool.at(pool_address)
    pool.add_liquidity(amount0, recipient, sender=alice, value=amount0)
    init_bal = alice.balance
    Factory.swap_out(pool_id, token, amount1,
                     alice.address, sender=Compass_EVM)
    assert alice.balance == init_bal + amount1


def test_withdraw_fee(Factory, Compass_EVM, project, alice, governance):
    pool_id = 0
    token = "0x0000000000000000000000000000000000000000"
    amount0 = 10 ** 16
    amount1 = 10 ** 15
    recipient = "recipient"
    Factory.create_pool(token, pool_id, sender=Compass_EVM)
    pool_address = Factory.pool_addresses(pool_id, token)
    pool = project.eth_pool.at(pool_address)
    pool.add_liquidity(amount0, recipient, sender=alice, value=amount0)
    init_bal = governance.balance
    Factory.withdraw_fee(pool_id, token, amount1, sender=Compass_EVM)
    assert governance.balance == init_bal + amount1
