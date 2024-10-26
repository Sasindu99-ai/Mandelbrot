# Mandelbrot Fractal Renderer with Pygame and Taichi
Interactive Mandelbrot fractal renderer using Pygame and Taichi. Features include dynamic texture swapping, real-time controls for zoom and movement, customizable rendering quality, and smooth performance with Taichi kernels. Perfect for exploring fractal visuals with adjustable detail and style.

## Features

- **Dynamic Texture Swapping**: Press `C` to cycle through various textures for different visual styles.
- **Real-Time Navigation**: Control zoom, movement, and rendering quality with keyboard inputs.
- **Optimized Rendering**: Powered by Taichi kernels for smooth rendering and high-resolution visuals.

## Controls

| Key    | Action                         |
|--------|--------------------------------|
| `W`    | Move up                        |
| `S`    | Move down                      |
| `A`    | Move left                      |
| `D`    | Move right                     |
| `↑`    | Zoom in                        |
| `↓`    | Zoom out                       |
| `←`    | Decrease max iterations        |
| `→`    | Increase max iterations        |
| `C`    | Change texture                 |
| `R`    | Recenter                       |
| `Z`    | Auto zoom out to center        |

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/Sasindu99-ai/Mandelbrot.git
    cd Mandelbrot
    ```
2. Install dependencies:
    ```bash
    make install
    ```

## Running the Application

To start the renderer, run:
```bash
make run
```
