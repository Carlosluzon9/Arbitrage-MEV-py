// SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../interfaces/IUniswapV2Router02.sol";
import "../interfaces/ISwapRouter_Algebra.sol";
import "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";

contract Arbitrage {
    address internal immutable owner;
    using SafeERC20 for IERC20;
    error Unauthorized();

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
    ) public payable {
        // Used to allow Routers from Uniswap V2, Uniswap V3, etc.
        // the access to tokens held by this contract
        uint maxInt = type(uint256).max;

        uint tokensLength = tokens.length;
        uint protocolsLength = protocols.length;

        for (uint i; i < tokensLength; ) {
            IERC20 token = IERC20(tokens[i]);
            for (uint j; j < protocolsLength; ) {
                address protocol = protocols[j];
                token.safeApprove(protocol, maxInt);

                unchecked {
                    ++j;
                }
            }

            unchecked {
                ++i;
            }
        }
    }
}
