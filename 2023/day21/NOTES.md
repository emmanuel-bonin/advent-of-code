# Notes

## Known stuff

- Steps to compute: `26501365`

## Resolution steps

Initial grid:
.....
.###.
..S..
.###.
.....

[?] Compute the number of steps before starting looping

[?] Compute the first case of the exterior grid that is reached by a possibility when computing the steps above, and so for each side

[?] For each of those possibilities, compute the number of iterations before looping, but starting from the previously computed tile (the one that reached the outside first)

Expand the grid to have one more grid on each of its sides:

```code
..... ..... .....
.###. .###. .###.
..... ..... .....
.###. .###. .###.
..... ..... .....
..... ..... .....
.###. .###. .###.
..... ..S.. .....
.###. .###. .###.
..... ..... .....
..... ..... .....
.###. .###. .###.
..... ..... .....
.###. .###. .###.
..... ..... .....
```

Then compute the number of computations needed to start looping for the first central grid
