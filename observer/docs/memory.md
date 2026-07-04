#




## in our memory analysis, we analyzed based on the most important factors:
```
| Priority | Check                       | Why it matters                                                    |
| -------: | --------------------------- | ----------------------------------------------------------------- |
|        1 | Available memory            | Is the machine actually running out of usable RAM?                |
|        2 | Swap activity               | Is the kernel compensating by swapping?                           |
|        3 | PSI memory pressure         | Are tasks stalling because of memory pressure?                    |
|        4 | OOM / allocation failures   | Has memory exhaustion already occurred?                           |
|        5 | Page reclaim / scanning     | Is the kernel working hard to reclaim memory?                     |
|        6 | Commit ratio                | Has memory been overcommitted?                                    |
|        7 | Major page faults           | Is disk-backed paging hurting performance?                        |
|        8 | Cache vs application memory | Is high usage just filesystem cache or real application pressure? |
```

