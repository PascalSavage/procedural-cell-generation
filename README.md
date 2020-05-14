# Prodecural cell generation

We generated new cells using data from https://www.allencell.org/

### Prodecure

- Extract only membrane channel from hyperstack image
- Find shapes of cells using edge detector
- Floodfill cell area where the center of cell is selected by hand.
- Extract the 2d cell shape at each slice
- For each 2d shape find n landmarks e.g. 100 landmarks
- Join all 2d shapes of all slices to get 3d shape of the cell
- Make Point distribution model of landmarked cells
- Generate new cell using by randomizing eigen value of eigen vector

