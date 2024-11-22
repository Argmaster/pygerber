"""Library for handling test assets."""

from __future__ import annotations

import inspect
import logging
import subprocess
import time
from enum import Enum
from hashlib import sha1
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Generic, Optional, Sequence, TypeVar

import dulwich
import dulwich.porcelain
import dulwich.repo
import numpy as np
from attr import dataclass
from filelock import FileLock
from PIL import Image
from pydantic import BaseModel, DirectoryPath, Field, HttpUrl
from pydantic_core import Url

if TYPE_CHECKING:
    import cv2
    from typing_extensions import Self


AUTO_COMMIT_CHANGES = False


class Source(BaseModel):
    """Generic base class for representing asset sources."""

    def load(self) -> bytes:
        """Load the asset from the source."""
        raise NotImplementedError

    def update(self, content: bytes) -> None:
        """Update the asset from the source."""
        raise NotImplementedError


class GitRepository(BaseModel):
    """Git repository information."""

    remote: Optional[HttpUrl] = Field(default=None)
    """URL of the remote repository."""

    checkout_target: str
    """Branch, tag, or commit to checkout."""

    local_path: Optional[Path] = Field(default=None)

    @classmethod
    def new_remote(cls, remote: str, checkout_target: str) -> Self:
        """Create a new GitRepository instance."""
        return cls(remote=Url(remote), checkout_target=checkout_target)

    def file(self, path: str | Path) -> GitFile:
        """Get a GitFile instance for the repository."""
        return GitFile(
            repository=self, file_path=Path(path) if isinstance(path, str) else path
        )

    def uid(self) -> str:
        """Generate a unique identifier for the repository."""
        return unique_id(
            str(self.remote),
            self.checkout_target,
        )

    def get_clone_dest(self) -> Path:
        """Get the path to clone the repository to."""
        pytest_cache = Path.cwd() / ".pytest_cache"
        if not pytest_cache.exists():
            pytest_cache.mkdir(exist_ok=True, parents=True)

        return pytest_cache / f"{self.uid()}"

    def commit_changes(self, file: Path, message: str) -> None:
        """Commit changes to the repository."""
        repo = self.get_repository_path()

        logging.info(str(dulwich.porcelain.status(repo.as_posix())))

        dulwich.porcelain.add(repo.as_posix(), file.as_posix())
        dulwich.porcelain.commit(repo.as_posix(), message)

        logging.info(str(dulwich.porcelain.status(repo.as_posix())))

        result = subprocess.run(  # noqa: S603
            [  # noqa: S607
                "git",
                "push",
                "--set-upstream",
                "origin",
                self.checkout_target,
            ],
            cwd=repo.as_posix(),
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            logging.error("<> RETURN CODE:\n %s", result.returncode)
            logging.error("<> STDERR:\n %s", result.stderr.decode())
            logging.error("<> STDOUT:\n %s", result.stdout.decode())

    def get_repository_path(self) -> Path:
        """Get the path to the repository."""
        dest = self.local_path if self.local_path is not None else self.get_clone_dest()

        if dest.exists():
            return dest

        msg = f"Repository {self.remote} not found at {dest}"
        raise FileNotFoundError(msg)

    def get_clone_dest_lock_path(self) -> Path:
        """Get the path to the lock file for the clone destination."""
        return self.get_clone_dest().with_suffix(".lock")

    def get_dulwich_repository(self) -> dulwich.repo.Repo:
        """Get the dulwich repository object."""
        return dulwich.repo.Repo(self.get_clone_dest().as_posix())

    def init(self) -> Self:
        """Initialize the repository."""
        dest = self.get_clone_dest()
        self.local_path = dest
        lock = self.get_clone_dest_lock_path()

        if not dest.exists():
            with FileLock(lock.as_posix()):
                # Check if repository doesn't exist in case we were blocked by another process
                # which already created the repository
                if not dest.exists():
                    repo = dulwich.porcelain.clone(
                        str(self.remote), dest.as_posix(), depth=1
                    )
                    assert isinstance(repo, dulwich.repo.Repo)
                    dulwich.porcelain.checkout_branch(repo, self.checkout_target)
                    return self

        repo = self.get_dulwich_repository()
        with FileLock(lock.as_posix()):
            dulwich.porcelain.checkout_branch(repo, self.checkout_target)
            dulwich.porcelain.fetch(dest.as_posix(), str(self.remote))
            dulwich.porcelain.reset(repo, "hard", f"origin/{self.checkout_target}")
        return self


class GitFile(Source):
    """Asset source representing a git repository."""

    repository: GitRepository
    """Git repository information."""

    file_path: Path
    """Path to the file within the repository, relative to repository root."""

    def load(self) -> bytes:
        """Load the asset from the source."""
        root = self.repository.get_repository_path()
        src = root / self.file_path
        return src.read_bytes()

    def update(self, content: bytes) -> None:
        """Update the asset from the source."""
        root = self.repository.get_repository_path()
        dest = root / self.file_path
        dest.parent.mkdir(0o777, parents=True, exist_ok=True)
        dest.touch(0o777, exist_ok=True)
        dest.write_bytes(content)

        if AUTO_COMMIT_CHANGES:
            self.repository.commit_changes(
                dest, f"Update {self.file_path.as_posix()!r}"
            )


class Directory(BaseModel):
    """Asset source representing a file system location."""

    directory: DirectoryPath

    @classmethod
    def new(cls, directory: Path | str) -> Self:
        """Create a new Directory instance."""
        if isinstance(directory, str):
            directory = Path(directory)
        return cls(directory=directory.resolve())

    def file(self, path: str | Path) -> File:
        """Get a File instance for the directory."""
        return File(
            directory=self, file_path=Path(path) if isinstance(path, str) else path
        )


class File(Source):
    """Asset source representing a file system location."""

    directory: Directory
    """Directory information."""

    file_path: Path
    """Path to the file within the directory, relative to directory root."""

    def load(self) -> bytes:
        """Load the asset from the source."""
        src = self.absolute_path
        return src.read_bytes()

    def update(self, content: bytes) -> None:
        """Update the asset from the source."""
        dest = self.absolute_path
        dest.parent.mkdir(0o777, parents=True, exist_ok=True)
        dest.touch(0o777, exist_ok=True)
        dest.write_bytes(content)

    @property
    def absolute_path(self) -> Path:
        """Get the absolute path to the file."""
        return self.directory.directory / self.file_path


SourceT = TypeVar("SourceT", bound=Source)


class Asset(BaseModel, Generic[SourceT]):
    """Generic base class for representing assets."""

    src: SourceT
    """Source of the asset."""


class TextAsset(Asset[SourceT]):
    """Asset representing a text file."""

    encoding: str = "utf-8"

    def load(self) -> str:
        """Load the asset from the source."""
        return self.src.load().decode(encoding=self.encoding)

    def update(self, content: str) -> None:
        """Update the asset from the source."""
        self.src.update(content.encode(encoding=self.encoding))

    @classmethod
    def new(cls, src: SourceT) -> TextAsset[SourceT]:
        """Create a new TextAsset instance."""
        return cls(src=src)


class ImageFormat(Enum):
    """Enumeration of image formats."""

    BLP = "blp"
    BMP = "bmp"
    DDS = "dds"
    DIB = "dib"
    EPS = "eps"
    GIF = "gif"
    ICNS = "icns"
    ICO = "ico"
    IM = "im"
    JPEG = "jpeg"
    J2K = "j2k"
    JP2 = "jp2"
    JPX = "jpx"
    MSP = "msp"
    PCX = "pcx"
    PFM = "pfm"
    PNG = "png"
    PPM = "ppm"
    SGI = "sgi"
    SPIDER = "spider"
    TGA = "tga"
    TIFF = "tiff"
    WEBP = "webp"
    XBM = "xbm"


class ImageAsset(Asset[SourceT]):
    """Asset representing an image file."""

    image_format: ImageFormat

    def load(self) -> Image.Image:
        """Load the asset from the source."""
        raw = self.src.load()
        return Image.open(BytesIO(raw), formats=[self.image_format.value])

    def update(self, content: Image.Image) -> None:
        """Update the asset from the source."""
        io = BytesIO()
        content.save(io, format=self.image_format.value)
        self.src.update(io.getvalue())

    @classmethod
    def new(cls, src: SourceT, image_format: ImageFormat) -> ImageAsset[SourceT]:
        """Create a new ImageAsset instance."""
        return cls(src=src, image_format=image_format)


_LONG_ENOUGH_TO_HAVE_ONE_MORE_FRAME = 2


def this_directory(__file__: Optional[str] = None) -> Path:
    """Get the directory of the file that called this function."""
    if __file__ is not None:
        return Path(__file__).parent

    stack = inspect.stack()
    if len(stack) < _LONG_ENOUGH_TO_HAVE_ONE_MORE_FRAME:
        return Path.cwd()

    caller_frame = inspect.stack()[1]
    caller_filename = Path(caller_frame.filename)
    if caller_filename.is_file():
        return caller_filename.parent

    return Path.cwd()


class Analyzer:
    """Generic base class for analyzing assets for testing purposes."""


class ImageAnalyzer:
    """Analyzer for image assets."""

    def __init__(self, reference: Image.Image) -> None:
        self.reference = reference

    def histogram_compare_color(
        self, other: Image.Image, method: Optional[int] = None
    ) -> HistCompValues:
        """Compare the histograms of two color images."""
        import cv2

        if method is None:
            method = cv2.HISTCMP_CORREL

        img1 = np.array(self.reference)
        img2 = np.array(other)

        min_channels = min(img1.shape[-1], img2.shape[-1])
        correlations: list[float] = []

        for channel in range(min_channels):  # 0: Blue, 1: Green, 2: Red
            # Compute histograms
            hist1 = cv2.calcHist([img1], [channel], None, [256], [0, 256])  # type: ignore[list-item]
            hist2 = cv2.calcHist([img2], [channel], None, [256], [0, 256])  # type: ignore[list-item]

            # Normalize histograms
            hist1 = cv2.normalize(hist1, hist1).flatten()
            hist2 = cv2.normalize(hist2, hist2).flatten()

            # Compare histograms using different methods
            correlation = cv2.compareHist(hist1, hist2, method)
            correlations.append(correlation)

        return HistCompValues(channel=correlations)

    def structural_similarity(self, other: Image.Image) -> float:
        """Compute the structural similarity index between two images."""
        import skimage

        img1 = np.array(self.reference)
        img2 = np.array(other)

        similarity = skimage.metrics.structural_similarity(
            img1, img2, data_range=255, channel_axis=2
        )
        assert isinstance(similarity, float)

        return similarity

    def assert_same_size(
        self, other: Image.Image, x_tolerance: int = 0, y_tolerance: int = 0
    ) -> None:
        """Compare the size of two images."""
        assert abs(self.reference.size[0] - other.size[0]) <= x_tolerance
        assert abs(self.reference.size[1] - other.size[1]) <= y_tolerance


@dataclass
class KeyPointMatches:
    """Key point matches between two images."""

    matches: Sequence[cv2.DMatch]

    def assert_count(self, count: int) -> Self:
        """Expect the number of key point matches."""
        assert (
            len(self.matches) == count
        ), f"Expected {count} key point matches found, got {len(self.matches)}"
        return self


@dataclass
class HistCompValues:
    """Correlation values for comparing assets."""

    channel: list[float]

    def assert_channel_count(self, count: int) -> Self:
        """Expect the number of correlation values."""
        assert (
            len(self.channel) == count
        ), f"Expected {count} correlation values, got {len(self.channel)}"
        return self

    def assert_greater_or_equal_values(self, min_value: float) -> Self:
        """Expect the minimum value of the correlations."""
        for value in self.channel:
            assert (
                value >= min_value
            ), f"Expected correlation value >= {min_value}, got {value}"

        return self


def unique_id(*components: str) -> str:
    """Generate a unique identifier."""
    if components:
        return sha1("".join(components).encode()).hexdigest()  # noqa: S324
    return sha1(str(time.time()).encode()).hexdigest()  # noqa: S324
