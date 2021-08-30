# ASA State Observer
The ASA State Observer is an Algorand dApp that exposes a set of methods to
assert conditions on Account's ASAs state.

The ASA State Observer can be used in combination with other Apps or Contract
Accounts.

App calls to the ASA State Observer, for example, could be included in a 
Group Transaction, checked by Stateless ASC1, to verify that an Account's 
ASA state match some required conditions.

#### Dependencies:
- `pyteal` [0.7.0](https://github.com/algorand/pyteal/releases/tag/v0.7.0)


### App's Methods
Reference docs: [ARC-4](https://github.com/jannotti/ARCs/blob/abi/ARCs/arc-0004.md)

```json
{
  "name": "AsaOptedIn",
  "desc": "Asserts that the targetAccount opted-in the targetAsa",
  "accounts" : [
    { "name": "targetAccount" }
  ],
  "foreign-assets" : [
    { "name": "targetAsa" }
  ]
}
```
```json
{
  "name": "AsaAmountEq",
  "desc": "Asserts that the targetAccount owns an amount of targetAsa equal to amt",
  "args": [
    { "name": "amt", "type": "uint64", "desc": "Asset amount" }
  ],
  "accounts" : [
    { "name": "targetAccount" }
  ],
  "foreign-assets" : [
    { "name": "targetAsa" }
  ]
}
```
```json
{
  "name": "AsaAmountGt",
  "desc": "Asserts that the targetAccount owns an amount of targetAsa greter then amt",
  "args": [
    { "name": "amt", "type": "uint64", "desc": "Asset amount" }
  ],
  "accounts" : [
    { "name": "targetAccount" }
  ],
  "foreign-assets" : [
    { "name": "targetAsa" }
  ]
}
```
```json
{
  "name": "AsaAmountGe",
  "desc": "Asserts that the targetAccount owns an amount of targetAsa greter or equal to amt",
  "args": [
    { "name": "amt", "type": "uint64", "desc": "Asset amount" }
  ],
  "accounts" : [
    { "name": "targetAccount" }
  ],
  "foreign-assets" : [
    { "name": "targetAsa" }
  ]
}
```
```json
{
  "name": "AsaAmountLt",
  "desc": "Asserts that the targetAccount owns an amount of targetAsa less then amt",
  "args": [
    { "name": "amt", "type": "uint64", "desc": "Asset amount" }
  ],
  "accounts" : [
    { "name": "targetAccount" }
  ],
  "foreign-assets" : [
    { "name": "targetAsa" }
  ]
}
```
```json
{
  "name": "AsaAmountLe",
  "desc": "Asserts that the targetAccount owns an amount of targetAsa less or equal to amt",
  "args": [
    { "name": "amt", "type": "uint64", "desc": "Asset amount" }
  ],
  "accounts" : [
    { "name": "targetAccount" }
  ],
  "foreign-assets" : [
    { "name": "targetAsa" }
  ]
}
```

### App's Interface
Reference docs: [ARC-4](https://github.com/jannotti/ARCs/blob/abi/ARCs/arc-0004.md)
[...]


### ASA State Observer on TestNet
The ASA State Observer has been [deployed on TestNet](https://testnet.algoexplorer.io/application/24248443).

You can try the App with GOAL CLI calling the `AsaAmountGe` method to verify that a given `TARGET_ACCOUNT_ADDRESS` owns an amount of a given `TARGET_ASSET_ID` greter or equal to `0`:
```shell
./goal app call
--app-id 24248443
--from YOUR_ADDRESS
--app-account TARGET_ACCOUNT_ADDRESS
--app-arg "str:AsaAmountGe"
--app-arg "int:0"
--foreign-asset TARGET_ASSET_ID
```

### Unit Tests
The ASA State Observer methods has been tested with the [library `algoapp_method_unittest`](https://github.com/cusma/algoapp_method_unittest), to provide an example of app's methods unit tests.
