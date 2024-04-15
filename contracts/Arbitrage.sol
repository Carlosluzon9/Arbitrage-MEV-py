// SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/IUniswapV2Router02.sol";
import "../interfaces/ISwapRouter_Algebra.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";

interface ILBRouter {
    enum Version {
        V1,
        V2,
        V2_1
    }

    struct Path {
        uint256[] pairBinSteps;
        Version[] versions;
        IERC20[] tokenPath;
    }

    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        Path memory path,
        address to,
        uint256 deadline
    ) external returns (uint256 amountOut);
}

contract Arbitrage {
    address internal immutable owner;
    using SafeERC20 for IERC20;
    error Unauthorized();
    error noProfit();

    struct SwapParams {
        uint8 protocol;
        address handler;
        address tokenIn;
        address tokenOut;
        uint24 fee;
        uint256 amount;
        ILBRouter.Path path;
    }

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        _checkOwner();
        _;
    }

    function _checkOwner() internal view virtual {
        if (msg.sender != owner) {
            revert Unauthorized();
        }
    }

    function recoverMyTokens(
        address[] calldata tokenAddress
    ) external onlyOwner {
        for (uint i = 0; i < tokenAddress.length; i++) {
            IERC20 token = IERC20(tokenAddress[i]);
            token.safeTransfer(msg.sender, token.balanceOf(address(this)));
        }
    }

    function approveHandlers(
        address[] calldata tokens,
        address[] calldata protocols
    ) external {
        // Used to allow Routers from Uniswap V2, Uniswap V3, etc.
        // the access to tokens held by this contract
        uint maxInt = type(uint256).max;

        uint tokensLength = tokens.length;
        uint protocolsLength = protocols.length;

        for (uint i; i < tokensLength; ) {
            IERC20 token = IERC20(tokens[i]);
            for (uint j; j < protocolsLength; ) {
                address protocol = protocols[j];
                token.forceApprove(protocol, maxInt);

                unchecked {
                    ++j;
                }
            }

            unchecked {
                ++i;
            }
        }
    }

    function profitSwap(
        SwapParams[] calldata paramsArray,
        uint256 minAmountOut
    ) external onlyOwner {
        uint256 amountOut;
        uint256 paramsArrayLength = paramsArray.length;

        for (uint256 i; i < paramsArrayLength; ) {
            SwapParams memory params = paramsArray[i];
            IERC20 tokenIn = IERC20(params.tokenIn);
            uint256 allowanceIn = tokenIn.allowance(
                address(this),
                params.handler
            );
            if (allowanceIn == 0) {
                uint maxInt = type(uint256).max;
                tokenIn.forceApprove(params.handler, maxInt);
            }

            if (amountOut == 0) {
                amountOut = params.amount;
            } else {
                params.amount = amountOut;
            }

            if (params.protocol == 0) {
                amountOut = uniswapV2Swap(params);
            } else if (params.protocol == 1) {
                amountOut = uniswapV3Swap(params);
            } else if (params.protocol == 2) {
                amountOut = AlgebraV3Swap(params);
            } else if (params.protocol == 3) {
                amountOut = TraderJoeV2Swap(params);
            }

            unchecked {
                ++i;
            }
        }

        if (amountOut < minAmountOut) {
            revert noProfit();
        }
    }

    function uniswapV3Swap(
        SwapParams memory params
    ) internal returns (uint256 amountOut) {
        ISwapRouter.ExactInputSingleParams memory singleParams = ISwapRouter
            .ExactInputSingleParams({
                tokenIn: params.tokenIn,
                tokenOut: params.tokenOut,
                fee: params.fee,
                recipient: address(this),
                deadline: block.timestamp + 20,
                amountIn: params.amount,
                amountOutMinimum: 0,
                sqrtPriceLimitX96: 0
            });

        amountOut = ISwapRouter(params.handler).exactInputSingle(singleParams);
    }

    function uniswapV2Swap(
        SwapParams memory params
    ) internal returns (uint256 amountOut) {
        address[] memory path;
        path = new address[](2);
        path[0] = params.tokenIn;
        path[1] = params.tokenOut;

        uint[] memory amounts = IUniswapV2Router02(params.handler)
            .swapExactTokensForTokens(
                params.amount,
                0,
                path,
                address(this),
                block.timestamp + 20
            );

        return amounts[1];
    }

    function AlgebraV3Swap(
        SwapParams memory params
    ) internal returns (uint256 amountOut) {
        ISwapRouter_Algebra.ExactInputSingleParams
            memory singleParams = ISwapRouter_Algebra.ExactInputSingleParams({
                tokenIn: params.tokenIn,
                tokenOut: params.tokenOut,
                recipient: address(this),
                deadline: block.timestamp + 20,
                amountIn: params.amount,
                amountOutMinimum: 0,
                limitSqrtPrice: 0
            });

        amountOut = ISwapRouter_Algebra(params.handler).exactInputSingle(
            singleParams
        );
    }

    function TraderJoeV2Swap(
        SwapParams memory params
    ) internal returns (uint256 amountOut) {
        amountOut = ILBRouter(params.handler).swapExactTokensForTokens(
            params.amount,
            0,
            params.path,
            address(this),
            block.timestamp + 20
        );
    }
}
