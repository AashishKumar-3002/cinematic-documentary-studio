from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import studio_runtime as runtime

class RuntimeLookupChecks(unittest.TestCase):
    def setUp(self):
        cache=Path(__file__).resolve().parents[2]/'.cache/tests'
        cache.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=cache)
        self.root=Path(self.temp.name)
        self.bin=self.root/'tools/bin';self.bin.mkdir(parents=True)
        self.override=patch.object(runtime,'ROOT',self.root);self.override.start()

    def tearDown(self):
        self.override.stop();self.temp.cleanup()

    def test_windows_prefers_project_executable(self):
        exe=self.bin/'ffmpeg.exe';exe.write_bytes(b'test')
        with patch.object(runtime.platform,'system',return_value='Windows'),patch.object(runtime.shutil,'which',return_value='other'):
            self.assertEqual(runtime.find_tool('ffmpeg'),str(exe))

    def test_unix_uses_local_executable_without_exe_suffix(self):
        exe=self.bin/'ffmpeg';exe.write_text('#!/bin/sh\n');exe.chmod(0o755)
        with patch.object(runtime.platform,'system',return_value='Linux'),patch.object(runtime.os,'access',return_value=True):
            self.assertEqual(runtime.find_tool('ffmpeg'),str(exe))

    def test_macos_preserves_system_install_location(self):
        with patch.object(runtime.platform,'system',return_value='Darwin'),patch.object(runtime.shutil,'which',return_value='/opt/homebrew/bin/ffprobe'):
            self.assertEqual(runtime.find_tool('ffprobe'),'/opt/homebrew/bin/ffprobe')
            self.assertFalse((self.bin/'ffprobe').exists())

    def test_nonexecutable_unix_file_does_not_hide_path_tool(self):
        (self.bin/'ffprobe').write_bytes(b'not executable')
        with patch.object(runtime.platform,'system',return_value='Linux'),patch.object(runtime.os,'access',return_value=False),patch.object(runtime.shutil,'which',return_value='/usr/bin/ffprobe'):
            self.assertEqual(runtime.find_tool('ffprobe'),'/usr/bin/ffprobe')

    def test_missing_tool_has_actionable_error_and_optional_probe(self):
        with patch.object(runtime.shutil,'which',return_value=None):
            self.assertIsNone(runtime.find_tool('ffmpeg',required=False))
            with self.assertRaisesRegex(FileNotFoundError,'docs/SETUP.md'):runtime.find_tool('ffmpeg')

if __name__=='__main__':unittest.main()
