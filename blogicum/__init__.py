"""Compatibility package to support imports from repository root."""
import os

# Allow `import blogicum.settings` from repo root by exposing inner package.
__path__.append(os.path.join(os.path.dirname(__file__), 'blogicum'))
