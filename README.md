## Simplified Memory Bounded A*

A* is a search algorithm that finds the shortest path between nodes in a graph. But it is not memory friendly at all; to fix this, we can use a memory bounded A* algorithm or SMA* for short.

![Crossing a probably easier road...](https://media.giphy.com/media/xUPGcM9CazM9H5KrEA/giphy.gif)

### How it Works

Explaining how SMA* or her mother A* works is not easy in some short sentences. I saved some notes during my research in Notion, you can learn more about this algorithms through [this](https://ejqfnptjmbdvhfm3645zsena4u5jma.notion.site/Simplified-Memory-Bounded-A-2d8676c053bb4540ae3618d3d1564b43) page.

### Usage

Write down your map in the following format in a text file:

```
$      ###      #   #        # # #
       ### X        #
              #####          X
```

The letter `$` represents the start and the letter `X` represents the end point. You can also use the `#` characters as wall.

Then run the program by passing the path of the maze file:

```bash
python core.py <path_to_maze_file>
```

[Here](samples) is some sample mazes for you to quickly test the algorithm.

### License

This project is licensed under the MIT license found in the [LICENSE](LICENSE) file in the root directory of this repository.
