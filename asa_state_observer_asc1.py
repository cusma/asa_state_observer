"""
ASA State Observer

The ASA State Observer is an Algorand dApp that exposes a set of methods to
asserts conditions on Account's ASAs state.

The ASA State Observer can be used in combination with other Apps or Contract
Accounts.

App calls to the ASA State Observer, for example, could be included in a
Group Transaction, checked by Stateless ASC1, to verify that an Account's
ASA state match some required conditions.
"""

__author__ = "Cosimo Bassi <cosimo.bassi@algorand.com>"


from pyteal import *


TEAL_VERSION = 3
MAX_FEE = Int(1000)

# GLOBAL SCHEMA
GLOBAL_INTS = 0
GLOBAL_BYTES = 0

# LOCAL SCHEMA
LOCAL_INTS = 0
LOCAL_BYTES = 0

# METHODS
METHOD_ASA_OPTED_IN = 'AsaOptedIn'
METHOD_ASA_AMOUNT_EQ = 'AsaAmountEq'
METHOD_ASA_AMOUNT_GT = 'AsaAmountGt'
METHOD_ASA_AMOUNT_GE = 'AsaAmountGe'
METHOD_ASA_AMOUNT_LT = 'AsaAmountLt'
METHOD_ASA_AMOUNT_LE = 'AsaAmountLe'

TARGET_ACCOUNT = Int(1)
TARGET_ASSET = Txn.assets[0]
TARGET_ASSET_AMOUNT = Btoi(Txn.application_args[1])

# ARGUMENTS ARRAYS
NUM_ARGS_ASA_OPTED_IN = Int(1)
NUM_ARGS_ASA_AMOUNT_EQ = Int(2)
NUM_ARGS_ASA_AMOUNT_GT = Int(2)
NUM_ARGS_ASA_AMOUNT_GE = Int(2)
NUM_ARGS_ASA_AMOUNT_LT = Int(2)
NUM_ARGS_ASA_AMOUNT_LE = Int(2)


def compile_stateful(program):
    return compileTeal(program, Mode.Application, version=TEAL_VERSION)


def return_true():
    return Return(Int(1))


def return_false():
    return Return(Int(0))


def asa_opted_in():
    asa_balance = AssetHolding.balance(
        TARGET_ACCOUNT,
        TARGET_ASSET,
    )

    return Seq([
        Assert(Txn.application_args.length() == NUM_ARGS_ASA_OPTED_IN),

        asa_balance,
        Assert(asa_balance.hasValue()),

        return_true()
    ])


def asa_amount_eq():
    asa_balance = AssetHolding.balance(
        TARGET_ACCOUNT,
        TARGET_ASSET,
    )

    return Seq([
        Assert(Txn.application_args.length() == NUM_ARGS_ASA_AMOUNT_EQ),

        asa_balance,
        Assert(asa_balance.hasValue()),
        Assert(
            Eq(
                asa_balance.value(),
                TARGET_ASSET_AMOUNT,
            )
        ),

        return_true()
    ])


def asa_amount_gt():
    asa_balance = AssetHolding.balance(
        TARGET_ACCOUNT,
        TARGET_ASSET,
    )

    return Seq([
        Assert(Txn.application_args.length() == NUM_ARGS_ASA_AMOUNT_GT),

        asa_balance,
        Assert(asa_balance.hasValue()),
        Assert(
            Gt(
                asa_balance.value(),
                TARGET_ASSET_AMOUNT,
            )
        ),

        return_true()
    ])


def asa_amount_ge():
    asa_balance = AssetHolding.balance(
        TARGET_ACCOUNT,
        TARGET_ASSET,
    )

    return Seq([
        Assert(Txn.application_args.length() == NUM_ARGS_ASA_AMOUNT_GE),

        asa_balance,
        Assert(asa_balance.hasValue()),
        Assert(
            Ge(
                asa_balance.value(),
                TARGET_ASSET_AMOUNT,
            )
        ),

        return_true()
    ])


def asa_amount_lt():
    asa_balance = AssetHolding.balance(
        TARGET_ACCOUNT,
        TARGET_ASSET,
    )

    return Seq([
        Assert(Txn.application_args.length() == NUM_ARGS_ASA_AMOUNT_LT),

        asa_balance,
        Assert(asa_balance.hasValue()),
        Assert(
            Lt(
                asa_balance.value(),
                TARGET_ASSET_AMOUNT,
            )
        ),

        return_true()
    ])


def asa_amount_le():
    asa_balance = AssetHolding.balance(
        TARGET_ACCOUNT,
        TARGET_ASSET,
    )

    return Seq([
        Assert(Txn.application_args.length() == NUM_ARGS_ASA_AMOUNT_LE),

        asa_balance,
        Assert(asa_balance.hasValue()),
        Assert(
            Le(
                asa_balance.value(),
                TARGET_ASSET_AMOUNT,
            )
        ),

        return_true()
    ])


def calls():
    precondition = And(
        Txn.type_enum() == TxnType.ApplicationCall,
        # TODO: maybe checking rekey_to is unecessary
        Txn.rekey_to() == Global.zero_address(),
        Txn.application_args.length() >= Int(1),
        Txn.assets.length() == Int(1),
        Txn.accounts.length() == Int(1),
    )

    return Seq([
        Assert(precondition),

        Cond(
            [Txn.application_args[0] == Bytes(METHOD_ASA_OPTED_IN), asa_opted_in()],
            [Txn.application_args[0] == Bytes(METHOD_ASA_AMOUNT_EQ), asa_amount_eq()],
            [Txn.application_args[0] == Bytes(METHOD_ASA_AMOUNT_GT), asa_amount_gt()],
            [Txn.application_args[0] == Bytes(METHOD_ASA_AMOUNT_GE), asa_amount_ge()],
            [Txn.application_args[0] == Bytes(METHOD_ASA_AMOUNT_LE), asa_amount_le()],
            [Txn.application_args[0] == Bytes(METHOD_ASA_AMOUNT_LT), asa_amount_lt()],
        ),

        return_true(),
    ])


def asa_state_observer():
    return Cond(
        [Txn.application_id() == Int(0), return_true()],
        [Txn.on_completion() == OnComplete.NoOp, calls()],
        [Txn.on_completion() == OnComplete.OptIn, return_false()],
        [Txn.on_completion() == OnComplete.CloseOut, return_false()],
        [Txn.on_completion() == OnComplete.UpdateApplication, return_false()],
        [Txn.on_completion() == OnComplete.DeleteApplication, return_false()],
    )


def asa_state_observe_closeout_or_clear():
    return return_false()


if __name__ == "__main__":
    compile_stateful(asa_state_observer())
