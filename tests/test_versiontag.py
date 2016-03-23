import subprocess
import tempfile
import unittest
import os
import logging

import versiontag


def silent_call(*args):
    with open(os.devnull, 'wb') as devnull:
        subprocess.check_call(args, stdout=devnull, stderr=devnull)


class VersionTagTest(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.repo_dir = tempfile.TemporaryDirectory()
        os.chdir(self.repo_dir.name)

    def tearDown(self):
        self.repo_dir.cleanup()
        logging.disable(logging.NOTSET)

    def _set_author(self):
        silent_call('git', 'config', 'user.email', 'travis@example.com')
        silent_call('git', 'config', 'user.name', 'Travis von Builder')

    def test_no_repo(self):
        """No repo returns default version"""
        self.assertEqual(versiontag.get_version(), 'r0.0.0')
        self.assertEqual(versiontag.get_version(pypi=True), '0.0.0')

    def test_no_commits(self):
        """No tags returns default version"""
        silent_call('git', 'init')
        self._set_author()
        self.assertEqual(versiontag.get_version(), 'r0.0.0')
        self.assertEqual(versiontag.get_version(pypi=True), '0.0.0')

    def test_head_is_tagged(self):
        """Should return most recent tag"""
        silent_call('git', 'init')
        self._set_author()
        silent_call('git', 'commit', '--allow-empty', '-m', 'Initial Commit')
        silent_call('git', 'tag', 'r1.2.3')
        self.assertEqual(versiontag.get_version(), 'r1.2.3')
        self.assertEqual(versiontag.get_version(pypi=True), '1.2.3')

    def test_head_is_post_release(self):
        """Subsequent commits show as post releases"""
        silent_call('git', 'init')
        self._set_author()
        silent_call('git', 'commit', '--allow-empty', '-m', 'Initial Commit')
        silent_call('git', 'tag', 'r1.2.3')
        silent_call('git', 'commit', '--allow-empty', '-m', 'another commit')
        self.assertTrue( versiontag.get_version().startswith('r1.2.3-1-') )
        self.assertEqual(versiontag.get_version(pypi=True), '1.2.3-1')

        silent_call('git', 'commit', '--allow-empty', '-m', 'another commit')
        self.assertTrue(versiontag.get_version().startswith('r1.2.3-2-'))
        self.assertEqual(versiontag.get_version(pypi=True), '1.2.3-2')

        silent_call('git', 'tag', 'r1.2.4')
        self.assertTrue( versiontag.get_version().startswith('r1.2.4') )
        self.assertEqual(versiontag.get_version(pypi=True), '1.2.4')

    def test_caching_with_removed_git_folder(self):
        """Caching continues to return release even if git repository disappears"""
        silent_call('git', 'init')
        self._set_author()
        silent_call('git', 'commit', '--allow-empty', '-m', 'Initial Commit')
        silent_call('git', 'tag', 'r1.2.3')

        versiontag.cache_git_tag()

        self.assertTrue( versiontag.get_version().startswith('r1.2.3') )
        self.assertEqual(versiontag.get_version(pypi=True), '1.2.3')

        silent_call('rm', '-rf', os.path.join(self.repo_dir.name, '.git'))

        self.assertTrue( versiontag.get_version().startswith('r1.2.3') )
        self.assertEqual(versiontag.get_version(pypi=True), '1.2.3')

        # Remove the version cache file and get_version goes back to return the default
        silent_call('rm', os.path.join(self.repo_dir.name, 'version.txt'))

        self.assertEqual(versiontag.get_version(), 'r0.0.0')
        self.assertEqual(versiontag.get_version(pypi=True), '0.0.0')
