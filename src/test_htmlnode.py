import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})
    
    def test_props_to_html(self):
        node = HTMLNode(props={"class": "container", "id": "main"})
        props_html = node.props_to_html()
        self.assertIn(' class="container"', props_html)
        self.assertIn(' id="main"', props_html)

    def test_repr(self):
        node = HTMLNode(tag="p", value="Paragraph")
        expected_repr = "HTMLNode(tag=p, value=Paragraph, children=None, props=None)"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello world!")
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)
    
