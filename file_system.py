"""
Game File System
Manages the virtual file system for the game
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class GameFileSystem:
    """Virtual file system for the game"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.base_dir = Path(__file__).parent
        self.assets_dir = self.base_dir / "assets" / "story_files"
        
        # Virtual file system structure
        self.file_system = {}
        self.current_challenge = 1
        self.current_step = 1
        
        # Initialize basic structure
        self._initialize_base_structure()
    
    def setup_challenge(self, challenge: int, step: int):
        """Setup file system for specific challenge/step"""
        self.current_challenge = challenge
        self.current_step = step
        
        # Load challenge-specific file system modifications
        self._load_challenge_files(challenge, step)
    
    def apply_challenge_modifications(self, modifications: List[Dict]):
        """Apply a list of file system modifications"""
        for mod in modifications:
            action = mod.get("action")
            path = mod.get("path")
            
            if action == "remove":
                self.remove_item(path)
            elif action == "add":
                item_type = mod.get("type", "file")
                content = mod.get("content", "")
                permissions = mod.get("permissions", None)
                
                # If content is a filename reference, load the actual content
                if item_type == "file" and content and not content.startswith("["):
                    content = self._load_story_file(content)
                
                self.add_item(path, item_type, content, permissions)
            elif action == "chmod":
                # Change permissions on existing item
                permissions = mod.get("permissions", {})
                node = self._get_node(path)
                if node:
                    node["permissions"] = permissions
    
    def remove_item(self, path: str) -> bool:
        """Remove an item from the file system"""
        components = self._resolve_path(path)
        
        if len(components) < 2:
            return False
        
        # Navigate to parent directory
        parent_path = "/".join(components[:-1])
        if parent_path == "":
            parent_path = "~"
        
        parent_node = self._get_node(parent_path)
        if parent_node is None or parent_node.get("type") != "directory":
            return False
        
        item_name = components[-1]
        children = parent_node.get("children", {})
        
        if item_name not in children:
            return False
        
        # Remove item
        del children[item_name]
        return True
    
    def add_item(self, path: str, item_type: str, content: str = "", permissions: Dict = None) -> bool:
        """Add an item to the file system"""
        components = self._resolve_path(path)
        
        if len(components) < 2:
            return False
        
        # Navigate to parent directory
        parent_path = "/".join(components[:-1])
        if parent_path == "":
            parent_path = "~"
        
        parent_node = self._get_node(parent_path)
        if parent_node is None or parent_node.get("type") != "directory":
            return False
        
        item_name = components[-1]
        if "children" not in parent_node:
            parent_node["children"] = {}
        
        # Add item
        if item_type == "directory":
            new_item = {
                "type": "directory",
                "children": {}
            }
        else:
            new_item = {
                "type": "file",
                "content": content
            }
        
        # Set permissions if provided
        if permissions is not None:
            new_item["permissions"] = permissions
        
        parent_node["children"][item_name] = new_item
        return True
    
    def _initialize_base_structure(self):
        """Initialize the basic file system structure"""
        self.file_system = {
            "~": {
                "type": "directory",
                "children": {
                    "my-house": {
                        "type": "directory",
                        "children": {
                            "my-room": {
                                "type": "directory",
                                "children": {
                                    "alarm": {
                                        "type": "file",
                                        "content": self._load_story_file("alarm")
                                    },
                                    "bed": {
                                        "type": "file",
                                        "content": self._load_story_file("bed_my-room")
                                    },
                                    "wardrobe": {
                                        "type": "directory",
                                        "children": {
                                            "t-shirt": {
                                                "type": "file",
                                                "content": self._load_story_file("t-shirt")
                                            },
                                            "trousers": {
                                                "type": "file",
                                                "content": self._load_story_file("trousers")
                                            },
                                            "skirt": {
                                                "type": "file",
                                                "content": self._load_story_file("skirt")
                                            },
                                            "cap": {
                                                "type": "file",
                                                "content": self._load_story_file("cap")
                                            }
                                        }
                                    },
                                    "shelves": {
                                        "type": "directory",
                                        "children": {
                                            "comic-book": {
                                                "type": "file",
                                                "content": self._load_story_file("comic-book")
                                            },
                                            "note": {
                                                "type": "file",
                                                "content": self._load_story_file("note_my-room")
                                            }
                                        }
                                    },
                                    ".chest": {
                                        "type": "directory",
                                        "children": {
                                            "LS": {
                                                "type": "file",
                                                "content": self._load_story_file("LS")
                                            },
                                            "CAT": {
                                                "type": "file",
                                                "content": self._load_story_file("CAT")
                                            },
                                            "CD": {
                                                "type": "file",
                                                "content": self._load_story_file("CD")
                                            },
                                            ".note": {
                                                "type": "file",
                                                "content": self._load_story_file(".note")
                                            }
                                        }
                                    }
                                }
                            },
                            "kitchen": {
                                "type": "directory",
                                "children": {
                                    "table": {
                                        "type": "file",
                                        "content": self._load_story_file("table")
                                    },
                                    "oven": {
                                        "type": "file",
                                        "content": self._load_story_file("oven")
                                    },
                                    "Mum": {
                                        "type": "file",
                                        "content": self._load_story_file("Mum")
                                    },
                                    # Food items for challenge 10
                                    "banana": {
                                        "type": "file",
                                        "content": self._load_story_file("banana")
                                    },
                                    "cake": {
                                        "type": "file",
                                        "content": self._load_story_file("cake")
                                    },
                                    "croissant": {
                                        "type": "file",
                                        "content": self._load_story_file("croissant")
                                    },
                                    "grapes": {
                                        "type": "file",
                                        "content": self._load_story_file("grapes")
                                    },
                                    "milk": {
                                        "type": "file",
                                        "content": self._load_story_file("milk")
                                    },
                                    "newspaper": {
                                        "type": "file",
                                        "content": self._load_story_file("newspaper")
                                    },
                                    "pie": {
                                        "type": "file",
                                        "content": self._load_story_file("pie")
                                    },
                                    "sandwich": {
                                        "type": "file",
                                        "content": self._load_story_file("sandwich")
                                    }
                                }
                            },
                            "parents-room": {
                                "type": "directory",
                                "children": {
                                    "bed": {
                                        "type": "file",
                                        "content": self._load_story_file("bed_parents-room")
                                    },
                                    ".safe": {
                                        "type": "directory",
                                        "children": {
                                            "ECHO": {
                                                "type": "file",
                                                "content": self._load_story_file("ECHO")
                                            },
                                            "mums-diary": {
                                                "type": "file",
                                                "content": self._load_story_file("mums-diary")
                                            },
                                            "map": {
                                                "type": "file",
                                                "content": self._load_story_file("map")
                                            }
                                        }
                                    }
                                }
                            },
                            "garden": {
                                "type": "directory",
                                "children": {
                                    "flowers": {
                                        "type": "file",
                                        "content": self._load_story_file("flowers")
                                    },
                                    "greenhouse": {
                                        "type": "directory",
                                        "children": {
                                            "note": {
                                                "type": "file",
                                                "content": self._load_story_file("note_greenhouse")
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "town": {
                        "type": "directory",
                        "children": {
                            "Mayor": {
                                "type": "file",
                                "content": self._load_story_file("Mayor")
                            },
                            "grumpy-man": {
                                "type": "file",
                                "content": self._load_story_file("grumpy-man")
                            },
                            "young-girl": {
                                "type": "file",
                                "content": self._load_story_file("young-girl")
                            },
                            "little-boy": {
                                "type": "file",
                                "content": self._load_story_file("little-boy")
                            },
                            ".hidden-shelter": {
                                "type": "directory",
                                "children": {
                                    "Eleanor": {
                                        "type": "file",
                                        "content": self._load_story_file("Eleanor")
                                    },
                                    "Edward": {
                                        "type": "file",
                                        "content": self._load_story_file("Edward")
                                    },
                                    "Edith": {
                                        "type": "file",
                                        "content": self._load_story_file("Edith")
                                    },
                                    "dog": {
                                        "type": "file",
                                        "content": self._load_story_file("dog")
                                    },
                                    "apple": {
                                        "type": "file",
                                        "content": self._load_story_file("apple")
                                    },
                                    "basket": {
                                        "type": "directory",
                                        "children": {
                                            "empty-bottle": {
                                                "type": "file",
                                                "content": self._load_story_file("empty-bottle")
                                            }
                                        }
                                    },
                                    ".tiny-chest": {
                                        "type": "directory",
                                        "children": {
                                            "MV": {
                                                "type": "file",
                                                "content": self._load_story_file("MV")
                                            }
                                        }
                                    }
                                }
                            },
                            "east": {
                                "type": "directory",
                                "children": {
                                    "shed-shop": {
                                        "type": "directory",
                                        "children": {
                                            "Bernard": {
                                                "type": "file",
                                                "content": self._load_story_file("Bernard")
                                            },
                                            "best-shed-maker-in-the-world.sh": {
                                                "type": "file",
                                                "content": "mkdir shed"
                                            },
                                            "best-horn-in-the-world.sh": {
                                                "type": "file",
                                                "content": "eco \"Honk!\""
                                            },
                                            "basement": {
                                                "type": "directory",
                                                "children": {
                                                    "photocopier.sh": {
                                                        "type": "file",
                                                        "content": self._load_story_file("photocopier.sh")
                                                    },
                                                    "bernards-diary-1": {
                                                        "type": "file",
                                                        "content": self._load_story_file("bernards-diary-1")
                                                    },
                                                    "bernards-diary-2": {
                                                        "type": "file",
                                                        "content": self._load_story_file("bernards-diary-2")
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "library": {
                                        "type": "directory",
                                        "children": {
                                            "public-section": {
                                                "type": "directory",
                                                "children": {
                                                    "VI": {
                                                        "type": "file",
                                                        "content": self._load_story_file("NANO")  # Using NANO file content for now
                                                    }
                                                }
                                            },
                                            "private-section": {
                                                "type": "directory",
                                                "children": {},
                                                "locked": True
                                            }
                                        }
                                    },
                                    "restaurant": {
                                        "type": "directory",
                                        "children": {
                                            ".cellar": {
                                                "type": "directory",
                                                "children": {
                                                    "Clara": {
                                                        "type": "file",
                                                        "content": self._load_story_file("Clara")
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "farm": {
                        "type": "directory",
                        "children": {
                            "barn": {
                                "type": "directory",
                                "children": {
                                    "Ruth": {
                                        "type": "file",
                                        "content": self._load_story_file("Ruth")
                                    },
                                    "Cobweb": {
                                        "type": "file",
                                        "content": self._load_story_file("Cobweb")
                                    },
                                    "Daisy": {
                                        "type": "file",
                                        "content": self._load_story_file("Daisy")
                                    },
                                    "Trotter": {
                                        "type": "file",
                                        "content": self._load_story_file("Trotter")
                                    }
                                }
                            },
                            "farmhouse": {
                                "type": "directory",
                                "children": {
                                    "bed": {
                                        "type": "file",
                                        "content": self._load_story_file("bed_farmhouse")
                                    }
                                }
                            },
                            "toolshed": {
                                "type": "directory",
                                "children": {
                                    "MKDIR": {
                                        "type": "file",
                                        "content": self._load_story_file("MKDIR")
                                    },
                                    "spanner": {
                                        "type": "file",
                                        "content": self._load_story_file("spanner")
                                    },
                                    "hammer": {
                                        "type": "file",
                                        "content": self._load_story_file("hammer")
                                    },
                                    "saw": {
                                        "type": "file",
                                        "content": self._load_story_file("saw")
                                    },
                                    "tape-measure": {
                                        "type": "file",
                                        "content": self._load_story_file("tape-measure")
                                    }
                                }
                            }
                        }
                    },
                    "basket": {
                        "type": "directory", 
                        "children": {}
                    }
                }
            }
        }
    
    def _load_story_file(self, filename: str) -> str:
        """Load content from a story file"""
        file_path = self.assets_dir / filename
        
        if not file_path.exists():
            return f"[Story file '{filename}' not found]"
        
        try:
            with open(file_path, 'r') as f:
                return f.read().strip()
        except Exception as e:
            if self.debug:
                print(f"Error loading story file {filename}: {e}")
            return f"[Error loading '{filename}']"
    
    def _load_challenge_files(self, challenge: int, step: int):
        """Load challenge-specific file system modifications"""
        # For now, we'll keep the base structure
        # In a full implementation, this would modify the file system
        # based on challenge requirements
        pass
    
    def _resolve_path(self, path: str) -> List[str]:
        """Resolve a path to a list of components"""
        if path == "~":
            return ["~"]
        
        if path.startswith("~/"):
            path = path[2:]  # Remove ~/
            components = ["~"]
            if path:
                components.extend(path.split("/"))
            return components
        
        return path.split("/")
    
    def _get_node(self, path: str) -> Optional[Dict[str, Any]]:
        """Get a node from the file system"""
        components = self._resolve_path(path)
        
        current = self.file_system
        for i, component in enumerate(components):
            if component not in current:
                return None
            
            if i == len(components) - 1:
                # Last component - return the node itself
                return current[component]
            else:
                # Navigate deeper
                current = current[component]
                if current.get("type") == "directory" and "children" in current:
                    current = current["children"]
                else:
                    # Can't navigate through a file
                    return None
        
        return None
    
    def directory_exists(self, path: str) -> bool:
        """Check if a directory exists"""
        node = self._get_node(path)
        return node is not None and node.get("type") == "directory"
    
    def file_exists(self, path: str) -> bool:
        """Check if a file exists"""
        node = self._get_node(path)
        return node is not None and node.get("type") == "file"
    
    def list_directory(self, path: str, show_hidden: bool = False) -> Optional[List[str]]:
        """List contents of a directory"""
        node = self._get_node(path)
        
        if node is None or node.get("type") != "directory":
            return None
        
        # Check if directory is locked
        if node.get("locked", False):
            return []  # Return empty list for locked directories
        
        children = node.get("children", {})
        items = list(children.keys())
        
        # Filter hidden files if not showing hidden
        if not show_hidden:
            items = [item for item in items if not item.startswith('.')]
        
        return items
    
    def read_file(self, path: str) -> Optional[str]:
        """Read contents of a file"""
        node = self._get_node(path)
        
        if node is None or node.get("type") != "file":
            return None
        
        return node.get("content", "")
    
    def write_file(self, path: str, content: str) -> bool:
        """Write content to a file"""
        components = self._resolve_path(path)
        
        if len(components) < 2:
            return False
        
        # Navigate to parent directory
        parent_path = "/".join(components[:-1])
        if parent_path == "":
            parent_path = "~"
        
        parent_node = self._get_node(parent_path)
        if parent_node is None or parent_node.get("type") != "directory":
            return False
        
        # Create or update file
        filename = components[-1]
        if "children" not in parent_node:
            parent_node["children"] = {}
        
        parent_node["children"][filename] = {
            "type": "file",
            "content": content
        }
        
        return True
    
    def create_directory(self, path: str) -> bool:
        """Create a directory"""
        components = self._resolve_path(path)
        
        if len(components) < 2:
            return False
        
        # Navigate to parent directory
        parent_path = "/".join(components[:-1])
        if parent_path == "":
            parent_path = "~"
        
        parent_node = self._get_node(parent_path)
        if parent_node is None or parent_node.get("type") != "directory":
            return False
        
        # Check if directory already exists
        dirname = components[-1]
        if "children" not in parent_node:
            parent_node["children"] = {}
        
        if dirname in parent_node["children"]:
            return False  # Already exists
        
        # Create directory
        parent_node["children"][dirname] = {
            "type": "directory",
            "children": {}
        }
        
        return True
    
    def remove_file(self, path: str) -> bool:
        """Remove a file"""
        components = self._resolve_path(path)
        
        if len(components) < 2:
            return False
        
        # Navigate to parent directory
        parent_path = "/".join(components[:-1])
        if parent_path == "":
            parent_path = "~"
        
        parent_node = self._get_node(parent_path)
        if parent_node is None or parent_node.get("type") != "directory":
            return False
        
        filename = components[-1]
        children = parent_node.get("children", {})
        
        if filename not in children or children[filename].get("type") != "file":
            return False
        
        # Remove file
        del children[filename]
        return True
    
    def move_file(self, source_path: str, dest_path: str) -> bool:
        """Move a file from source to destination"""
        # Read source file
        source_node = self._get_node(source_path)
        if source_node is None or source_node.get("type") != "file":
            return False
        
        content = source_node.get("content", "")
        
        # Check if destination is a directory
        dest_node = self._get_node(dest_path)
        if dest_node and dest_node.get("type") == "directory":
            # Moving into directory
            source_components = self._resolve_path(source_path)
            filename = source_components[-1]
            dest_path = dest_path + "/" + filename
        
        # Write to destination
        if not self.write_file(dest_path, content):
            return False
        
        # Remove source
        return self.remove_file(source_path)

    def chmod(self, path: str, mode: str) -> bool:
        """Change permissions on a file or directory"""
        node = self._get_node(path)
        if node is None:
            return False
        
        # Initialize permissions if not present
        if "permissions" not in node:
            node["permissions"] = {"r": True, "w": True, "x": True}
        
        # Parse mode (+r, +w, +x, +rwx, -r, -w, -x, etc.)
        if mode.startswith("+"):
            flags = mode[1:]
            for flag in flags:
                if flag in ["r", "w", "x"]:
                    node["permissions"][flag] = True
                else:
                    return False  # Invalid flag
        elif mode.startswith("-"):
            flags = mode[1:]
            for flag in flags:
                if flag in ["r", "w", "x"]:
                    node["permissions"][flag] = False
                else:
                    return False  # Invalid flag
        else:
            return False  # Invalid mode format
        
        return True
    
    def has_permission(self, path: str, permission: str) -> bool:
        """Check if a path has a specific permission (r, w, or x)"""
        node = self._get_node(path)
        if node is None:
            return False
        
        # If no permissions set, default to all allowed
        if "permissions" not in node:
            return True
        
        return node.get("permissions", {}).get(permission, False)
    
    def get_permissions_string(self, path: str) -> str:
        """Get permission string like 'drwxr-xr-x' for ls -l"""
        node = self._get_node(path)
        if node is None:
            return "----------"
        
        is_dir = node.get("type") == "directory"
        perms = node.get("permissions", {"r": True, "w": True, "x": True})
        
        # Build permission string
        perm_str = "d" if is_dir else "-"
        perm_str += "r" if perms.get("r", True) else "-"
        perm_str += "w" if perms.get("w", True) else "-"
        perm_str += "x" if perms.get("x", True) else "-"
        perm_str += "r-xr-x"  # Simplified: group and other permissions
        
        return perm_str

    def remove_directory_recursive(self, path: str) -> bool:
        """Remove a directory and all its contents"""
        components = self._resolve_path(path)
        
        if len(components) < 2:
            return False
        
        # Navigate to parent directory
        parent_path = "/".join(components[:-1])
        if parent_path == "":
            parent_path = "~"
        
        parent_node = self._get_node(parent_path)
        if parent_node is None or parent_node.get("type") != "directory":
            return False
        
        dirname = components[-1]
        children = parent_node.get("children", {})
        
        if dirname not in children or children[dirname].get("type") != "directory":
            return False
        
        # Remove directory
        del children[dirname]
        return True
