// SPDX-License-Identifier: None
pragma solidity ^0.8.4;

import "../interfaces/IUniswapV2Router02.sol";
import "../interfaces/ISwapRouter_Quickswap.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
//import "@uniswap/v2-periphery/contracts/interfaces/IUniswapV2Router02.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Arb is Ownable(msg.sender) {
    using SafeERC20 for IERC20;
    error no_profit(uint256 profit, uint256 min_profit);

    function V2Swap(
        address _router,
        address _tokenIn,
        address _tokenOut,
        uint256 _amountIn,
        uint256 _amountOutMin
    ) private returns (uint256) {
        IERC20(_tokenIn).forceApprove(_router, _amountIn);
        address[] memory path;
        path = new address[](2);
        path[0] = _tokenIn;
        path[1] = _tokenOut;
        uint256 deadline = block.timestamp + 100;
        uint256[] memory amountOut2;

        amountOut2 = IUniswapV2Router02(_router).swapExactTokensForTokens(
            _amountIn,
            _amountOutMin,
            path,
            address(this),
            deadline
        );

        return amountOut2[1];
    }

    function V2feeSwap(
        address _router,
        address _tokenIn,
        address _tokenOut,
        uint256 _amountIn,
        uint256 _amountOutMin
    ) private returns (uint256) {
        uint256 initialBalance = IERC20(_tokenOut).balanceOf(address(this));
        IERC20(_tokenIn).forceApprove(_router, _amountIn);
        address[] memory path;
        path = new address[](2);
        path[0] = _tokenIn;
        path[1] = _tokenOut;
        uint256 deadline = block.timestamp + 100;
        IUniswapV2Router02(_router)
            .swapExactTokensForTokensSupportingFeeOnTransferTokens(
                _amountIn,
                _amountOutMin,
                path,
                address(this),
                deadline
            );
        uint256 balanceOut = IERC20(_tokenOut).balanceOf(address(this)) -
            initialBalance;
        return balanceOut;
    }

    function V3Swap(
        address _router,
        address _tokenIn,
        address _tokenOut,
        uint256 _amountIn,
        uint256 _amountOutMin,
        uint24 _fee
    ) private returns (uint256) {
        IERC20(_tokenIn).forceApprove(_router, _amountIn);
        uint256 deadline = block.timestamp + 100;
        uint256 amountOut3;
        if (_fee == 0) {
            amountOut3 = ISwapRouter_quickswap(_router).exactInputSingle(
                ISwapRouter_quickswap.ExactInputSingleParams({
                    tokenIn: _tokenIn,
                    tokenOut: _tokenOut,
                    recipient: address(this),
                    deadline: deadline,
                    amountIn: _amountIn,
                    amountOutMinimum: _amountOutMin,
                    limitSqrtPrice: 0
                })
            );
        } else {
            amountOut3 = ISwapRouter(_router).exactInputSingle(
                ISwapRouter.ExactInputSingleParams({
                    tokenIn: _tokenIn,
                    tokenOut: _tokenOut,
                    fee: _fee,
                    recipient: address(this),
                    deadline: deadline,
                    amountIn: _amountIn,
                    amountOutMinimum: _amountOutMin,
                    sqrtPriceLimitX96: 0
                })
            );
        }
        return amountOut3;
    }

    function V2V2Swap(
        address Router1,
        address Router2,
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 amountOutMin1,
        uint256 amountOutMin2
    ) external onlyOwner {
        uint256 amountOut = V2Swap(
            Router1,
            tokenIn,
            tokenOut,
            amountIn,
            amountOutMin1
        );
        uint256 amountOut2 = V2Swap(
            Router2,
            tokenOut,
            tokenIn,
            amountOut,
            amountOutMin2
        );

        if (amountOut2 < amountIn) {
            revert no_profit(amountOut2, amountIn);
        }
    }

    function V2V3Swap(
        address Router1,
        address Router2,
        address tokenIn,
        address tokenOut,
        uint24 fee2,
        uint256 amountIn,
        uint256 amountOutMin1,
        uint256 amountOutMin2
    ) external onlyOwner {
        uint256 amountOut = V2Swap(
            Router1,
            tokenIn,
            tokenOut,
            amountIn,
            amountOutMin1
        );
        uint256 amountOut2 = V3Swap(
            Router2,
            tokenOut,
            tokenIn,
            amountOut,
            amountOutMin2,
            fee2
        );

        if (amountOut2 < amountIn) {
            revert no_profit(amountOut2, amountIn);
        }
    }

    function V3V2Swap(
        address Router1,
        address Router2,
        address tokenIn,
        address tokenOut,
        uint24 fee1,
        uint256 amountIn,
        uint256 amountOutMin1,
        uint256 amountOutMin2
    ) external onlyOwner {
        uint256 amountOut = V3Swap(
            Router1,
            tokenIn,
            tokenOut,
            amountIn,
            amountOutMin1,
            fee1
        );
        uint256 amountOut2 = V2Swap(
            Router2,
            tokenOut,
            tokenIn,
            amountOut,
            amountOutMin2
        );

        if (amountOut2 < amountIn) {
            revert no_profit(amountOut2, amountIn);
        }
    }

    function V3V3Swap(
        address Router1,
        address Router2,
        address tokenIn,
        address tokenOut,
        uint24 fee1,
        uint24 fee2,
        uint256 amountIn,
        uint256 amountOutMin1,
        uint256 amountOutMin2
    ) external onlyOwner {
        uint256 amountOut = V3Swap(
            Router1,
            tokenIn,
            tokenOut,
            amountIn,
            amountOutMin1,
            fee1
        );
        uint256 amountOut2 = V3Swap(
            Router2,
            tokenOut,
            tokenIn,
            amountOut,
            amountOutMin2,
            fee2
        );

        if (amountOut2 < amountIn) {
            revert no_profit(amountOut2, amountIn);
        }
    }

    function feeOnToken(
        address Router1,
        address Router2,
        address tokenIn,
        address tokenOut,
        uint24 fee1,
        uint24 fee2,
        uint256 amountIn,
        uint256 amountOutMin1,
        uint256 amountOutMin2,
        uint16 swaptype
    ) external onlyOwner {
        uint256 amountOut2;

        if (swaptype == 0) {
            uint256 amountOut1 = V2feeSwap(
                Router1,
                tokenIn,
                tokenOut,
                amountIn,
                amountOutMin1
            );
            amountOut2 = V2feeSwap(
                Router2,
                tokenOut,
                tokenIn,
                amountOut1,
                amountOutMin2
            );
        } else if (swaptype == 1) {
            uint256 amountOut1 = V2feeSwap(
                Router1,
                tokenIn,
                tokenOut,
                amountIn,
                amountOutMin1
            );
            amountOut2 = V3Swap(
                Router2,
                tokenOut,
                tokenIn,
                amountOut1,
                amountOutMin2,
                fee2
            );
        } else if (swaptype == 2) {
            uint256 amountOut1 = V3Swap(
                Router1,
                tokenIn,
                tokenOut,
                amountIn,
                amountOutMin1,
                fee1
            );

            amountOut2 = V2feeSwap(
                Router2,
                tokenOut,
                tokenIn,
                amountOut1,
                amountOutMin2
            );
        } else {
            uint256 amountOut1 = V3Swap(
                Router1,
                tokenIn,
                tokenOut,
                amountIn,
                amountOutMin1,
                fee1
            );
            amountOut2 = V3Swap(
                Router2,
                tokenOut,
                tokenIn,
                amountOut1,
                amountOutMin2,
                fee2
            );
        }

        if (amountOut2 < amountIn) {
            revert no_profit(amountOut2, amountIn);
        }
    }

    function recoverEth() external onlyOwner {
        payable(msg.sender).transfer(address(this).balance);
    }

    function recoverMyTokens(
        address[] calldata tokenAddress
    ) external onlyOwner {
        for (uint i = 0; i < tokenAddress.length; i++) {
            IERC20 token = IERC20(tokenAddress[i]);
            token.safeTransfer(msg.sender, token.balanceOf(address(this)));
        }
    }
}
