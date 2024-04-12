pragma solidity ^0.8.20;

import "./ILBRouter.sol";

interface LBQuoter {
    struct Quote {
        address[] route;
        address[] pairs;
        uint256[] binSteps;
        ILBRouter.Version[] versions;
        uint128[] amounts;
        uint128[] virtualAmountsWithoutSlippage;
        uint128[] fees;
    }

    function findBestPathFromAmountIn(
        address[] calldata route,
        uint128 amountIn
    ) external view returns (Quote memory quote);
}
