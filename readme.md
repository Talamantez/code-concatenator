Use:

From the command line:

```python concatenator.py /path/to/your/project --output combined_code.txt --extensions .py .js .tsx --exclude-dirs node_modules test```

Or import it in you Python code:

```from concatenator import concatenate_code

concatenate_code(
    directory="./my_project",
    output_file="combined_code.txt",
    extensions=['.py', '.js', '.tsx'],
    exclude_dirs=['node_modules', 'test']
)```

PowerShell Profile Setup:

# First, save the Python script to a permanent location
$scriptDir = "$env:USERPROFILE\Scripts"
$pythonScript = @'
import os
from pathlib import Path
import argparse

def concatenate_code(directory, output_file, extensions=None, exclude_dirs=None):
    if extensions is None:
        extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp']
    
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', 'venv', '.git', '__pycache__', 'build', 'dist']

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(directory)
                    
                    outfile.write(f"\n{'='*80}\n")
                    outfile.write(f"File: {rel_path}\n")
                    outfile.write(f"{'='*80}\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Error reading file: {e}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate code files in a project')
    parser.add_argument('directory', help='Root directory of the project')
    parser.add_argument('--output', default='concatenated_code.txt', help='Output file path')
    parser.add_argument('--extensions', nargs='+', help='File extensions to include (e.g. .py .js)')
    parser.add_argument('--exclude-dirs', nargs='+', help='Directories to exclude')
    
    args = parser.parse_args()
    
    concatenate_code(
        args.directory,
        args.output,
        extensions=args.extensions,
        exclude_dirs=args.exclude_dirs
    )
'@

# Create the installation script
$installScript = @'
# Create Scripts directory if it doesn't exist
if (-not (Test-Path $env:USERPROFILE\Scripts)) {
    New-Item -ItemType Directory -Path $env:USERPROFILE\Scripts
}

# Save the Python script
$pythonScript | Out-File -FilePath "$env:USERPROFILE\Scripts\code_concatenator.py" -Encoding utf8

# Create or append to PowerShell profile
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

# Add the function to the profile
$profileContent = @'
function Concatenate-Code {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Directory,
        
        [Parameter(Mandatory=$false)]
        [string]$Output = "concatenated_code.txt",
        
        [Parameter(Mandatory=$false)]
        [string[]]$Extensions,
        
        [Parameter(Mandatory=$false)]
        [string[]]$ExcludeDirs
    )
    
    $cmd = "python `"$env:USERPROFILE\Scripts\code_concatenator.py`" `"$Directory`" --output `"$Output`""
    
    if ($Extensions) {
        $cmd += " --extensions $($Extensions -join ' ')"
    }
    
    if ($ExcludeDirs) {
        $cmd += " --exclude-dirs $($ExcludeDirs -join ' ')"
    }
    
    Invoke-Expression $cmd
}
'@

Add-Content $PROFILE $profileContent

Write-Host "Installation complete! Please restart PowerShell to use the new command."
Write-Host "Usage: Concatenate-Code -Directory 'path/to/project' [-Output 'output.txt'] [-Extensions @('.py', '.js')] [-ExcludeDirs @('node_modules')]"
'@

# Save and run the installation script
$installScript | Out-File "$env:TEMP\install_concatenator.ps1" -Encoding utf8

To install the global function:

Open PowerShell as Administrator
Copy the entire script above and save it as install_concatenator.ps1
Run the script:
```.\install_concatenator.ps1```
Restart PowerShell

After installation, you can use the function anywhere in PowerShell like this:

# Basic usage
Concatenate-Code -Directory "C:\MyProject"

# With all options
Concatenate-Code -Directory "C:\MyProject" `
                -Output "combined.txt" `
                -Extensions @(".py", ".js", ".tsx") `
                -ExcludeDirs @("node_modules", "tests")


Detailed use:

First, create a folder called "Scripts" in your user folder:

New-Item -ItemType Directory -Path "$env:USERPROFILE\Scripts"

Save this Python file as code_concatenator.py in that Scripts folder:

notepad "$env:USERPROFILE\Scripts\code_concatenator.py"
(The Python code from before goes in this file)

Set up the PowerShell profile by running:

if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}
notepad $PROFILE

Add this function to your PowerShell profile file that opens:

function Concatenate-Code {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Directory,
        
        [Parameter(Mandatory=$false)]
        [string]$Output = "concatenated_code.txt",
        
        [Parameter(Mandatory=$false)]
        [string[]]$Extensions,
        
        [Parameter(Mandatory=$false)]
        [string[]]$ExcludeDirs
    )
    
    $pythonScript = "$env:USERPROFILE\Scripts\code_concatenator.py"
    $cmd = "python `"$pythonScript`" `"$Directory`" --output `"$Output`""
    
    if ($Extensions) {
        $cmd += " --extensions $($Extensions -join ' ')"
    }
    
    if ($ExcludeDirs) {
        $cmd += " --exclude-dirs $($ExcludeDirs -join ' ')"
    }
    
    Invoke-Expression $cmd
}

Restart PowerShell

Would you like me to walk you through any of these steps in more detail? I can also share the Python code again if needed!
After this is set up, you can run the command from anywhere like:
Concatenate-Code -Directory "C:\Your\Project\Path"

Test Script:

# Create a test project structure
$testDir = ".\test_project"
New-Item -ItemType Directory -Force -Path $testDir
New-Item -ItemType Directory -Force -Path "$testDir\src"
New-Item -ItemType Directory -Force -Path "$testDir\utils"

# Create some test files with different extensions
@"
def main():
    print('Hello from main')

if __name__ == '__main__':
    main()
"@ | Out-File -FilePath "$testDir\src\main.py" -Encoding utf8

@"
export const helper = () => {
    console.log('Helper function');
};
"@ | Out-File -FilePath "$testDir\utils\helper.js" -Encoding utf8

@"
import React from 'react';

const App = () => {
    return <div>Hello World</div>;
};

export default App;
"@ | Out-File -FilePath "$testDir\src\App.tsx" -Encoding utf8

# Run the concatenator
Concatenate-Code -Directory $testDir -Output "test_output.txt"

# Display the result
Get-Content "test_output.txt"