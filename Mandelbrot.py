import time
from typing import List

import numpy as np
import pygame as pg
import taichi as ti
from pygame.key import ScancodeWrapper

import Global
from Global import appSpeed, height, maxIter, maxIterLimit, offset, scale, width, zoom
from Texture import Texture

__all__ = ['Mandelbrot']


@ti.data_oriented
class Mandelbrot:
    """
	Mandelbrot class to render the mandelbrot set

	Attributes:
	-----------
	app: App
		The app instance
	screenArray: NDArray
		The screen array
	texture: Texture
		The texture instance
	textures: List[Texture]
		The list of textures
	textureField: ti.Vector.field
		The texture field
	lastCEvent: float
		The last change event time
	keyPressBlocked: bool
		The key press blocked status
	autoZoomOutStartPoints: List[float]
		The auto zoom out start points (zoom, x, y, maxIter)

	Methods:
	--------
	changeTexture() -> None:
		Changes the texture
	deltaTime() -> float:
		Returns the delta time
	render(max_iter: int, zoom: float, dx: float, dy: float) -> None:
		Renders the mandelbrot set
	control() -> None:
		Controls the movement and zoom
	update() -> None:
		Updates the screen
	draw() -> None:
		Draws the screen
	run() -> None:
		Runs the app
	reCenter() -> None:
		Recenter the image
	"""
    textures = [Texture(i) for i in range(1, 11)]
    textureField: ti.Vector.field
    lastCEvent = time.time()
    keyPressBlocked: bool = False
    autoZoomOutStartPoints: List[float] = [0.0, 0.0, 0.0, 0.0]

    def __init__(self, app):
        """
		Initialize the fractal
		:param app: The app instance
		:type app: App.App
		"""
        self.app = app
        # screen array
        self.screenArray = np.full(shape=(width, height, 3), fill_value=[0, 0, 0], dtype=np.uint32)
        # taichi init
        ti.init(arch=ti.arm64)

        # texture
        self.texture = self.textures[1]

        # screen field
        self.screenField = ti.Vector.field(3, ti.uint32, (width, height))
        # texture field
        self.textureField = ti.Vector.field(3, ti.uint32, self.texture.get_size())
        self.textureField.from_numpy(self.texture.array)

        # mandelbrot set configurations
        self.vel = 0.01
        self.zoom, self.scale = zoom, scale
        self.increment = ti.Vector([0.0, 0.0])
        self.maxIter, self.maxIterLimit = maxIter, maxIterLimit

        # delta_time
        self.appSpeed = appSpeed
        self.prevTime = pg.time.get_ticks()

    def changeTexture(self) -> None:
        """
		Changes the texture
		:return: None
		"""
        nextIndex = (self.textures.index(self.texture) + 1) % len(self.textures)
        self.texture = self.textures[nextIndex]
        self.textureField.from_numpy(self.texture.array)

    def deltaTime(self) -> float:
        """
		Returns the delta time
		:return: float: The delta time
		"""
        now = pg.time.get_ticks() - self.prevTime
        self.prevTime = now
        return now * self.appSpeed

    @ti.kernel
    def render(self, maxIterations: ti.int32, zoomLevel: ti.float32, dx: ti.float32, dy: ti.float32):
        """
		Renders the mandelbrot set
		:param maxIterations: ti.int32: The maximum number of iterations
		:param zoomLevel: ti.float32: The zoom factor
		:param dx: ti.float32: The x offset
		:param dy: ti.float32: The y offset
		:return: None
		"""
        for x, y in self.screenField:
            # Complex number
            c = ti.Vector([(x - offset[0]) * zoomLevel - dx, (y - offset[1]) * zoomLevel - dy])
            # z = 0
            z = ti.Vector([0.0, 0.0])
            # Mandelbrot set
            lastIter = 0
            for i in range(maxIterations):
                z = ti.Vector([(z.x**2 - z.y**2 + c.x), (2 * z.x * z.y + c.y)])
                if z.dot(z) > 4:
                    break
                lastIter = i
            # Color
            col = int(self.texture.size * (lastIter + 1) / maxIterations)
            # Set the color
            self.screenField[x, y] = self.textureField[col, col]

    def control(self) -> None:
        """
		Controls the movement and zoom
		:return: None
		"""
        if self.keyPressBlocked:
            return

        # key events
        keyEvent = pg.key.get_pressed()

        # change texture
        if keyEvent[pg.K_c] and time.time() - self.lastCEvent > 0.5:
            self.lastCEvent = time.time()
            self.changeTexture()

        # recenter
        if keyEvent[pg.K_r] and time.time() - self.lastCEvent > 0.5:
            self.lastCEvent = time.time()
            self.reCenter()

        # auto zoom out to center
        if keyEvent[pg.K_z] and time.time() - self.lastCEvent > 0.5:
            self.lastCEvent = time.time()
            self.autoZoomOutStartPoints = [self.zoom, self.increment[0], self.increment[1], self.maxIter]
            self.autoZoomOutToCenter()

        # movement
        self.controlMovements(keyEvent)

        # zoom
        self.controlZooming(keyEvent)

        # max iterations (quality)
        self.controlMaxIterations(keyEvent)

    def controlMovements(self, keyEvent: ScancodeWrapper) -> None:
        """
		Controls the movements
		:param keyEvent: ScancodeWrapper: The key event
		:return: None
		"""
        dt = self.deltaTime()
        if keyEvent[pg.K_a]:
            self.increment[0] += self.vel * dt
        if keyEvent[pg.K_d]:
            self.increment[0] -= self.vel * dt
        if keyEvent[pg.K_w]:
            self.increment[1] += self.vel * dt
        if keyEvent[pg.K_s]:
            self.increment[1] -= self.vel * dt

    def controlZooming(self, keyEvent: ScancodeWrapper) -> None:
        """
		Controls the zooming
		:param keyEvent: ScancodeWrapper: The key event
		:return: None
		"""
        if keyEvent[pg.K_UP] or keyEvent[pg.K_DOWN]:
            invScale = 2 - self.scale
            if keyEvent[pg.K_UP]:
                self.zoom *= self.scale
                self.vel *= self.scale
            if keyEvent[pg.K_DOWN]:
                self.zoom *= invScale
                self.vel *= invScale

    def controlMaxIterations(self, keyEvent: ScancodeWrapper) -> None:
        """
		Controls the max iterations
		:param keyEvent: ScancodeWrapper: The key event
		:return: None
		"""
        if keyEvent[pg.K_LEFT]:
            self.maxIter -= 1
        if keyEvent[pg.K_RIGHT]:
            self.maxIter += 1
        self.maxIter = min(max(self.maxIter, 2), self.maxIterLimit)

    def update(self) -> None:
        """
		Updates the screen
		:return: None
		"""
        self.control()
        self.render(self.maxIter, self.zoom, self.increment[0], self.increment[1])
        self.screenArray = self.screenField.to_numpy()

    def draw(self) -> None:
        """
		Draws the screen
		:return: None
		"""
        pg.surfarray.blit_array(self.app.screen, self.screenArray)

    def run(self) -> None:
        """
		Runs the app
		:return: None
		"""
        if self.keyPressBlocked:
            self.autoZoomOutToCenter()
        self.update()
        self.draw()
        pg.display.flip()

    def reCenter(self) -> None:
        """
		Recenter the image
		:return: None
		"""
        self.increment = ti.Vector([0.0, 0.0])
        self.zoom = zoom
        self.vel = 0.01
        self.maxIter = maxIter
        self.textureField.from_numpy(self.texture.array)
        self.lastCEvent = time.time()
        self.run()

    def autoZoomOutToCenter(self) -> None:
        """
		Auto zoom out to center
		:return: None
		"""
        if self.zoom > Global.zoom or Global.zoom - self.autoZoomOutStartPoints[0] == 0:
            return

        self.keyPressBlocked = True

        invScale = 2 - self.scale

        self.zoom *= invScale
        self.vel *= invScale

        improvement = (Global.zoom - self.zoom) / (Global.zoom - self.autoZoomOutStartPoints[0])

        self.increment[0] = self.autoZoomOutStartPoints[1] * improvement
        self.increment[1] = self.autoZoomOutStartPoints[2] * improvement

        if self.autoZoomOutStartPoints[3] > Global.maxIter:
            self.maxIter = int(Global.maxIter + (self.autoZoomOutStartPoints[3] - Global.maxIter) * improvement)
            self.maxIter = min(max(self.maxIter, 2), self.maxIterLimit)

        if self.zoom > Global.zoom:
            self.keyPressBlocked = False
