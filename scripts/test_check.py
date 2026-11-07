import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check  # noqa: E402

YT = "https://www.youtube.com/watch?v=MTHGoGUFpvE"


def write(text):
    d = tempfile.mkdtemp()
    p = Path(d) / "note.md"
    p.write_text(text)
    return p


class CheckTests(unittest.TestCase):
    def test_untagged_section_fails(self):
        p = write("# T\n\n## Pods\n\nSome text.\n")
        self.assertTrue(check.check_source_tags(p))

    def test_tagged_section_passes(self):
        p = write(
            "# T\n\n## Probes\n<!-- chapter: Probes -->\n"
            f"[video 51:01]({YT}&t=3061s)\n\n"
            "## Etcd backup\nhttps://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/\n"
        )
        self.assertEqual(check.check_source_tags(p), [])
        self.assertEqual(check.check_timestamps(p), [])

    def test_helm_url_only_section_passes(self):
        p = write("## Helm\nhttps://helm.sh/docs/intro/using_helm/\n")
        self.assertEqual(check.check_source_tags(p), [])

    def test_lf_and_cncf_urls_pass(self):
        for u in ("https://training.linuxfoundation.org/certification/x/",
                  "https://docs.linuxfoundation.org/tc-docs/certification/x",
                  "https://github.com/cncf/curriculum/blob/main/x.pdf"):
            p = write(f"## S\n{u}\n")
            self.assertEqual(check.check_source_tags(p), [], u)

    def test_lookalike_urls_fail(self):
        for u in ("https://training.linuxfoundation.org.evil.com/x",
                  "https://github.com/someone-else/curriculum/x"):
            p = write(f"## S\n{u}\n")
            self.assertTrue(check.check_source_tags(p), u)

    def test_unrelated_domain_section_fails(self):
        p = write("## Helm\nhttps://example.com/docs/\n")
        self.assertTrue(check.check_source_tags(p))

    def test_timestamp_outside_declared_chapter_fails(self):
        p = write(
            "## Probes\n<!-- chapter: Probes -->\n"
            f"[video 02:00]({YT}&t=120s)\n"
        )
        self.assertTrue(check.check_timestamps(p))

    def test_unknown_chapter_fails(self):
        p = write(f"## X\n<!-- chapter: Nope -->\n[video 51:01]({YT}&t=3061s)\n")
        self.assertTrue(check.check_timestamps(p))

    def test_unbalanced_mermaid_fence_fails(self):
        p = write("## A\n```mermaid\ngraph TD\n  A-->B\n")
        self.assertTrue(check.check_mermaid(p))

    def test_mermaid_unknown_type_fails(self):
        p = write("## A\n```mermaid\nhello\n```\n")
        self.assertTrue(check.check_mermaid(p))

    def test_mermaid_ok(self):
        p = write("## A\n```mermaid\ngraph TD\n  A-->B\n```\n")
        self.assertEqual(check.check_mermaid(p), [])

    def test_denylist_flags_cube_control(self):
        p = write("Run Cube Control get pods\n")
        self.assertTrue(check.check_denylist(p))

    def test_denylist_clean(self):
        p = write("Run kubectl get pods; kubelet; etcd\n")
        self.assertEqual(check.check_denylist(p), [])

    def test_denylist_etc_d_case_and_word_bounds(self):
        self.assertEqual(check.check_denylist(write("pods, services, etc deploy later\n")), [])
        self.assertEqual(check.check_denylist(write("and so on, etc debug\n")), [])
        self.assertTrue(check.check_denylist(write("backup etc D snapshot\n")))
        self.assertTrue(check.check_denylist(write("backup etc D\n")))
        self.assertEqual(check.check_denylist(write("etc Deployment\n")), [])

    def test_chapter_ranges(self):
        self.assertEqual(check.CHAPTERS["Architecture"], (102, 1262))
        self.assertEqual(check.CHAPTERS["Continued Training"], (9914, 10207))
        self.assertEqual(len(check.CHAPTERS), 25)


if __name__ == "__main__":
    unittest.main()
