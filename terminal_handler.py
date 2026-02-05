"""
Terminal Handler
Processes and executes terminal commands in the game environment
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, List


class TerminalHandler:
    """Handles terminal command execution and validation"""
    
    def __init__(self, file_system, debug: bool = False):
        self.file_system = file_system
        self.debug = debug
        self.current_dir = "~"
        
        # Supported commands
        self.commands = {
            'ls': self._cmd_ls,
            'cd': self._cmd_cd,
            'cat': self._cmd_cat,
            'pwd': self._cmd_pwd,
            'mkdir': self._cmd_mkdir,
            'echo': self._cmd_echo,
            'mv': self._cmd_mv,
            'rm': self._cmd_rm,
            'vi': self._cmd_vi,
            'chmod': self._cmd_chmod,
            'sudo': self._cmd_sudo,
        }
    
    def set_current_directory(self, directory: str):
        """Set the current directory"""
        self.current_dir = directory
    
    def get_current_directory(self) -> str:
        """Get the current directory"""
        return self.current_dir
    
    def get_prompt(self) -> str:
        """Get the terminal prompt string"""
        # Simplify the directory display
        display_dir = self.current_dir
        if display_dir.startswith("~/"):
            display_dir = display_dir[2:]  # Remove ~/
        elif display_dir == "~":
            display_dir = ""
        
        return f"player@terminal:{display_dir}$"
    
    def _normalize_path(self, path: str, relative_to: str = None) -> str:
        """Normalize a path, handling . and .. references"""
        if relative_to is None:
            relative_to = self.current_dir
        
        # Handle absolute paths
        if path.startswith("~/"):
            components = path[2:].split("/") if path != "~/" else []
            base = ["~"]
        elif path == "~":
            return "~"
        elif path.startswith("/"):
            # Absolute path from root (treat as ~)
            components = path[1:].split("/") if path != "/" else []
            base = ["~"]
        else:
            # Relative path - start from current directory
            if relative_to == "~":
                base = ["~"]
            else:
                base = relative_to.split("/")
            components = path.split("/")
        
        # Process components, handling . and ..
        result = base.copy()
        for component in components:
            if component == "" or component == ".":
                # Skip empty and current directory references
                continue
            elif component == "..":
                # Go up one level (but not above ~)
                if len(result) > 1:
                    result.pop()
            else:
                result.append(component)
        
        # Reconstruct path
        if len(result) == 1 and result[0] == "~":
            return "~"
        return "/".join(result)
    
    def execute_command(self, command_line: str) -> Tuple[bool, str]:
        """Execute a command and return (success, output)"""
        if not command_line.strip():
            return True, ""
        
        # Parse command and arguments
        parts = command_line.strip().split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Handle script execution (commands starting with ./)
        if cmd.startswith("./"):
            return self._execute_script(cmd[2:])
        
        # Handle output redirection for echo
        output_file = None
        if '>' in parts:
            redirect_index = parts.index('>')
            if redirect_index < len(parts) - 1:
                output_file = parts[redirect_index + 1]
                # Remove redirection from args
                parts = parts[:redirect_index]
                args = parts[1:] if len(parts) > 1 else []
        
        # Execute command
        if cmd in self.commands:
            try:
                result = self.commands[cmd](args, output_file)
                return True, result
            except Exception as e:
                error_msg = f"Error executing {cmd}: {str(e)}"
                if self.debug:
                    import traceback
                    error_msg += f"\n{traceback.format_exc()}"
                return False, error_msg
        else:
            return False, f"Command not found: {cmd}"
    
    def _execute_script(self, script_name: str) -> Tuple[bool, str]:
        """Execute a script file"""
        # Resolve script path
        if not script_name.startswith("~/"):
            if self.current_dir == "~":
                script_path = "~/" + script_name
            else:
                script_path = self.current_dir + "/" + script_name
        else:
            script_path = script_name
        
        # Check if script exists
        content = self.file_system.read_file(script_path)
        if content is None:
            return False, f"bash: ./{script_name}: No such file or directory"
        
        # Check execute permission
        if not self.file_system.has_permission(script_path, "x"):
            return False, f"bash: ./{script_name}: Permission denied"
        
        # Execute each line in the script
        lines = content.strip().split('\n')
        output_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                success, result = self.execute_command(line)
                if result:
                    output_lines.append(result)
                if not success:
                    return False, result
        
        return True, '\n'.join(output_lines)
    
    def _cmd_ls(self, args: List[str], output_file: str = None) -> str:
        """List directory contents"""
        # Check for flags
        show_hidden = False
        long_format = False
        target_dir = "."
        
        if args:
            if "-a" in args:
                show_hidden = True
                args = [arg for arg in args if arg != "-a"]
            if "-l" in args:
                long_format = True
                args = [arg for arg in args if arg != "-l"]
            if args:
                target_dir = args[0]
        
        # Remove trailing slash if present (except for root)
        if target_dir.endswith("/") and target_dir != "/":
            target_dir = target_dir[:-1]
        
        # Normalize the path (handles . and ..)
        target_dir = self._normalize_path(target_dir)
        
        # Check read permission
        if not self.file_system.has_permission(target_dir, "r"):
            return f"ls: cannot open directory '{target_dir}': Permission denied"
        
        # Get directory contents from file system
        contents = self.file_system.list_directory(target_dir, show_hidden=show_hidden)
        
        if contents is None:
            return f"ls: cannot access '{args[0] if args else '.'}': No such file or directory"
        
        # Format output
        if not contents:
            return ""
        
        # Long format with permissions
        if long_format:
            result_lines = []
            for item in contents:
                item_path = target_dir + "/" + item if target_dir != "~" else "~/" + item
                perms = self.file_system.get_permissions_string(item_path)
                result_lines.append(f"{perms} player {item}")
            return "\n".join(result_lines)
        
        # Simple listing
        return "  ".join(contents)
    
    def _cmd_cd(self, args: List[str], output_file: str = None) -> str:
        """Change directory"""
        if not args:
            self.current_dir = "~"
            return ""
        
        target_dir = args[0]
        
        # Normalize the path (handles . and ..)
        new_path = self._normalize_path(target_dir)
        
        # Check if directory exists and has execute permission
        if not self.file_system.directory_exists(new_path):
            return f"cd: {target_dir}: No such file or directory"
        if not self.file_system.has_permission(new_path, "x"):
            return f"cd: {target_dir}: Permission denied"
        
        self.current_dir = new_path
        return ""
    
    def _cmd_cat(self, args: List[str], output_file: str = None) -> str:
        """Display file contents"""
        if not args:
            return "cat: missing file operand"
        
        filename = args[0]
        
        # Resolve file path
        if not filename.startswith("~/"):
            if self.current_dir == "~":
                filepath = "~/" + filename
            else:
                filepath = self.current_dir + "/" + filename
        else:
            filepath = filename
        
        # Check read permission
        if not self.file_system.has_permission(filepath, "r"):
            return f"cat: {filename}: Permission denied"
        
        # Get file contents
        content = self.file_system.read_file(filepath)
        
        if content is None:
            return f"cat: {filename}: No such file or directory"
        
        return content
    
    def _cmd_pwd(self, args: List[str], output_file: str = None) -> str:
        """Print working directory"""
        return self.current_dir
    
    def _cmd_mkdir(self, args: List[str], output_file: str = None) -> str:
        """Create directory"""
        if not args:
            return "mkdir: missing operand"
        
        dirname = args[0]
        
        # Resolve directory path
        if not dirname.startswith("~/"):
            if self.current_dir == "~":
                dirpath = "~/" + dirname
            else:
                dirpath = self.current_dir + "/" + dirname
        else:
            dirpath = dirname
        
        # Create directory
        success = self.file_system.create_directory(dirpath)
        
        if not success:
            return f"mkdir: cannot create directory '{dirname}': File exists"
        
        return ""
    
    def _cmd_echo(self, args: List[str], output_file: str = None) -> str:
        """Echo text"""
        text = " ".join(args)
        
        # Remove quotes if present
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        elif text.startswith("'") and text.endswith("'"):
            text = text[1:-1]
        
        # Handle output redirection
        if output_file:
            # Resolve file path
            if not output_file.startswith("~/"):
                if self.current_dir == "~":
                    filepath = "~/" + output_file
                else:
                    filepath = self.current_dir + "/" + output_file
            else:
                filepath = output_file
            
            # Write to file
            success = self.file_system.write_file(filepath, text)
            if not success:
                return f"echo: cannot write to '{output_file}'"
            return ""
        else:
            return text
    
    def _cmd_mv(self, args: List[str], output_file: str = None) -> str:
        """Move/rename file"""
        if len(args) < 2:
            return "mv: missing file operand"
        
        source = args[0]
        dest = args[1]
        
        # Handle wildcard (*)
        if '*' in source:
            # Get the directory part
            if '/' in source:
                dir_part = source.rsplit('/', 1)[0]
                dir_path = self._normalize_path(dir_part)
            else:
                dir_path = self.current_dir
            
            # Get all items in the directory
            items = self.file_system.list_directory(dir_path, show_hidden=False)
            if items is None:
                return f"mv: cannot access '{source}': No such file or directory"
            
            # Move each item
            for item in items:
                item_path = dir_path + "/" + item if dir_path != "~" else "~/" + item
                dest_path = self._normalize_path(dest)
                success = self.file_system.move_file(item_path, dest_path)
                if not success:
                    return f"mv: cannot move '{item}' to '{dest}'"
            
            return ""
        
        # Normalize source and destination paths (handles . and ..)
        source_path = self._normalize_path(source)
        dest_path = self._normalize_path(dest)
        
        # Move file
        success = self.file_system.move_file(source_path, dest_path)
        
        if not success:
            return f"mv: cannot move '{source}' to '{dest}'"
        
        return ""
        
        return ""
    
    def _cmd_rm(self, args: List[str], output_file: str = None) -> str:
        """Remove file"""
        if not args:
            return "rm: missing operand"
        
        filename = args[0]
        
        # Resolve file path
        if not filename.startswith("~/"):
            if self.current_dir == "~":
                filepath = "~/" + filename
            else:
                filepath = self.current_dir + "/" + filename
        else:
            filepath = filename
        
        # Remove file
        success = self.file_system.remove_file(filepath)
        
        if not success:
            return f"rm: cannot remove '{filename}': No such file or directory"
        
        return ""
    
    def _cmd_vi(self, args: List[str], output_file: str = None) -> str:
        """Simple text editor (simplified vi replacement)"""
        if not args:
            return "vi: missing file operand"
        
        filename = args[0]
        
        # Resolve file path
        if not filename.startswith("~/"):
            if self.current_dir == "~":
                filepath = "~/" + filename
            else:
                filepath = self.current_dir + "/" + filename
        else:
            filepath = filename
        
        # Read current content
        current_content = self.file_system.read_file(filepath)
        
        if current_content is None:
            return f"vi: {filename}: No such file or directory"
        
        # For the simplified version, we'll do a specific replacement for the horn script
        if filename == "best-horn-in-the-world.sh":
            # Replace "eco" with "echo" 
            new_content = current_content.replace("eco ", "echo ")
            
            # Write the corrected content back
            success = self.file_system.write_file(filepath, new_content)
            
            if success:
                return f"File {filename} has been edited and saved."
            else:
                return f"vi: cannot write to '{filename}'"
        else:
            return f"vi: {filename}: File opened in read-only mode (no changes made)"

    def _cmd_chmod(self, args: List[str], output_file: str = None) -> str:
        """Change file permissions (simplified)"""
        if len(args) < 2:
            return "chmod: missing operand\nTry 'chmod +r filename' or 'chmod +rwx filename'"
        
        mode = args[0]
        target = args[1].rstrip('/')
        
        # Resolve path
        if not target.startswith("~/"):
            if self.current_dir == "~":
                filepath = "~/" + target
            else:
                filepath = self.current_dir + "/" + target
        else:
            filepath = target
        
        # Check if target exists
        node = self.file_system._get_node(filepath)
        if node is None:
            return f"chmod: cannot access '{target}': No such file or directory"
        
        # Apply permission change
        success = self.file_system.chmod(filepath, mode)
        if success:
            return ""  # chmod succeeds silently
        else:
            return f"chmod: invalid mode: '{mode}'"

    def _cmd_sudo(self, args: List[str], output_file: str = None) -> str:
        """Execute command as super user (simplified)"""
        if not args:
            return "sudo: missing command"
        
        # Simple password check (in real game, would prompt for password)
        # For simplicity, we'll just execute the command
        # In a real implementation, you'd prompt for password first
        
        # Execute the sudo command
        cmd = args[0]
        cmd_args = args[1:] if len(args) > 1 else []
        
        # Handle rm -r specially for sudo
        if cmd == "rm" and cmd_args and cmd_args[0] == "-r":
            # Remove directory recursively
            if len(cmd_args) < 2:
                return "rm: missing operand"
            
            target = cmd_args[1].rstrip('/')
            
            # Resolve path
            if not target.startswith("~/"):
                if self.current_dir == "~":
                    filepath = "~/" + target
                else:
                    filepath = self.current_dir + "/" + target
            else:
                filepath = target
            
            # Remove directory and all contents
            success = self.file_system.remove_directory_recursive(filepath)
            if success:
                return ""
            else:
                return f"rm: cannot remove '{target}': No such file or directory"
        
        # For other commands, execute normally
        if cmd in self.commands:
            return self.commands[cmd](cmd_args, output_file)
        else:
            return f"sudo: {cmd}: command not found"
