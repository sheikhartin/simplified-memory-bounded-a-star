## Simplified Memory Bounded A*

A* is a search algorithm that finds the shortest path between nodes in a graph. However, it is not memory friendly at all and to fix this, we can use a memory bounded A* algorithm or SMA* for short.

![Maybe there was a better path with lower f-cost...](https://media.giphy.com/media/MRWCFJXVNyc8es2rHO/giphy.gif)

### How it Works

Explaining how SMA* or her mother A* works is not easy in some short sentences. I saved some notes during my research in Notion, you can learn more about this algorithms through [this](https://ejqfnptjmbdvhfm3645zsena4u5jma.notion.site/Simplified-Memory-Bounded-A-2d8676c053bb4540ae3618d3d1564b43) page.

### Usage

Save your custom maze in the following format in a text file:

```
$      ###      #   #        # # #
       ### X        #
              #####          X
```

The characters `$`/`S`/`s` represents the start and the `*`/`X`/`x`/`E`/`e`/`G`/`g` represents the end point. You can also use the `#`/`&`/`;` characters as wall.

Run the program by passing the path of the maze file:

```bash
python core.py -m <path_to_maze_file>
```

Use the `-g` flag to generate a random maze:

```bash
python core.py -g
```

<i>The generated maze will be saved in the `genmaze.txt` file in the current directory.</i>

Set the memory bound by the `-b` option:

```bash
python core.py -m genmaze.txt -b <memory_bound>
```

<i>Memory bound is not the storage bound in kilobyte or megabyte, it is the number of nodes that visited in the search.</i>

Force the program to continue searching even if the memory bound is reached:

```bash
python core.py -m samples/maze09.txt -b 100 -f
```

[Here](samples) is some sample mazes for you to quickly test the algorithm.

### License

This project is licensed under the MIT license found in the [LICENSE](LICENSE) file in the root directory of this repository.
