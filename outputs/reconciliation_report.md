```markdown
# Reconciliation Summary

**Matched Transactions:** 120
**Reconciliation Rate:** 73.68%

## Missing in ERP
No transactions are missing from ERP.

## Missing in Bank
The following transactions are present in ERP but missing in the bank statement:
- Invoice ID: INV0002, Amount: 1789.75
- Invoice ID: INV0028, Amount: 1815.57
- Invoice ID: INV0034, Amount: 1729.63
- Invoice ID: INV0041, Amount: 530.12
- Invoice ID: INV0050, Amount: 149.06
- Invoice ID: INV0051, Amount: 365.08
- Invoice ID: INV0055, Amount: 1863.27
- Invoice ID: INV0063, Amount: 1622.7
- Invoice ID: INV0069, Amount: 1485.12
- Invoice ID: INV0079, Amount: 344.12
- Invoice ID: INV0085, Amount: 1150.56
- Invoice ID: INV0091, Amount: 377.19
- Invoice ID: INV0093, Amount: 1885.87
- Invoice ID: INV0096, Amount: 1036.62
- Invoice ID: INV0101, Amount: 789.03
- Invoice ID: INV0110, Amount: 619.67
- Invoice ID: INV0113, Amount: 1631.73
- Invoice ID: INV0128, Amount: 1122.69
- Invoice ID: INV0131, Amount: 570.76
- Invoice ID: INV0142, Amount: 1745.92
- Invoice ID: INV0158, Amount: 126.87
- Invoice ID: INV0163, Amount: 226.09
- Invoice ID: INV0171, Amount: 510.42
- Invoice ID: INV0173, Amount: 1703.66
- Invoice ID: INV0175, Amount: 1584.61
- Invoice ID: INV0179, Amount: 80.77
- Invoice ID: INV0191, Amount: 1742.78
- Invoice ID: INV0197, Amount: 1494.89
- Invoice ID: INV0199, Amount: 1885.74
- Invoice ID: INV0200, Amount: 353.38
These transactions need to be investigated to determine why they are not present in the bank statement.

## Amount Mismatch
The following transactions have amount discrepancies between ERP and the bank statement:
- ERP Invoice ID: INV0002, ERP Amount: 1789.75, Bank Amount: 1788.62
- ERP Invoice ID: INV0178, ERP Amount: 390.27, Bank Amount: 391.43
- ERP Invoice ID: INV0181, ERP Amount: 262.66, Bank Amount: 263.79
- ERP Invoice ID: INV0195, ERP Amount: 1237.54, Bank Amount: 1236.63
- ERP Invoice ID: INV0170, ERP Amount: 1004.23, Bank Amount: 1003.71
These discrepancies could be due to rounding errors, incorrect data entry, or other factors.

## Duplicates
The following transactions appear as duplicates in the bank statement:
- Bank Ref ID: 17, Amount: 1992.44
- Bank Ref ID: 21, Amount: 365.02
- Bank Ref ID: 55, Amount: 1863.27
- Bank Ref ID: 62, Amount: 801.13
- Bank Ref ID: 110, Amount: 619.67
- Bank Ref ID: 132, Amount: 1947.64
- Bank Ref ID: 136, Amount: 186.13
- Bank Ref ID: 145, Amount: 1090.56
These duplicates should be investigated to ensure that they are not being double-counted.

## Non-Invoice Transactions
The following transactions in the bank statement do not correspond to invoices:
- Bank Ref ID: 1000, Description: Adjustment, Amount: -37.76
- Bank Ref ID: 1001, Description: Interest, Amount: -28.15
- Bank Ref ID: 1002, Description: Adjustment, Amount: -37.71
- Bank Ref ID: 1003, Description: Bank Fee, Amount: -34.47
- Bank Ref ID: 1004, Description: Adjustment, Amount: -19.48
- Bank Ref ID: 1005, Description: Interest, Amount: -26.29
- Bank Ref ID: 1006, Description: Adjustment, Amount: -40.08
- Bank Ref ID: 1007, Description: Interest, Amount: -49.65
- Bank Ref ID: 1008, Description: Bank Fee, Amount: -40.49
- Bank Ref ID: 1009, Description: Interest, Amount: -38.5
- Bank Ref ID: 1010, Description: Adjustment, Amount: -49.65
- Bank Ref ID: 1011, Description: Interest, Amount: -42.09
- Bank Ref ID: 1012, Description: Adjustment, Amount: -18.33
- Bank Ref ID: 1013, Description: Interest, Amount: -12.5
- Bank Ref ID: 1014, Description: Adjustment, Amount: -32.13
- Bank Ref ID: 1015, Description: Interest, Amount: -30.37
- Bank Ref ID: 1016, Description: Interest, Amount: -46.5
- Bank Ref ID: 1017, Description: Interest, Amount: -30.68
- Bank Ref ID: 1018, Description: Interest, Amount: -21.19
- Bank Ref ID: 1019, Description: Interest, Amount: -31.77
These transactions typically represent bank fees, interest, or other adjustments.

## Date Difference
No transactions have date differences.

