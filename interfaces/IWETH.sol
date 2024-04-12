pragma solidity 0.7.6;

interface IWETH {
    function withdraw(uint256 value) external;
    function deposit() external payable;
    function approve(address spender, uint256 value) external returns (bool);
}
