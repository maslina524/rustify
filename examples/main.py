from rustify import Result, assert_eq

ok = Result.ok(5)
ret = ok.map(lambda x: x * 2)
assert_eq(ret.unwrap(), 10)