package com.amigadeia;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

/**
 * PythonBridge - A simple bridge to call Python modules from Java
 * 
 * This class provides methods to call Python scripts and modules
 * that are stored in the app's assets folder.
 */
public class PythonBridge {
    
    private String pythonExecutablePath;
    private String pythonModulesPath;
    
    /**
     * Creates a new PythonBridge instance
     * 
     * @param pythonExecutablePath The path to the Python executable (e.g., "/data/data/com.amigadeia/files/python/bin/python3")
     * @param pythonModulesPath The path where Python modules are stored (e.g., "/data/data/com.amigadeia/files/python_modules")
     */
    public PythonBridge(String pythonExecutablePath, String pythonModulesPath) {
        this.pythonExecutablePath = pythonExecutablePath;
        this.pythonModulesPath = pythonModulesPath;
    }
    
    /**
     * Calls a Python module and function with specified arguments
     * 
     * @param moduleName The Python module name (without .py extension)
     * @param functionName The function name to call
     * @param args Arguments to pass to the function
     * @return The output from the Python function
     * @throws IOException If an error occurs during execution
     */
    public String callPythonFunction(String moduleName, String functionName, String... args) throws IOException {
        List<String> command = new ArrayList<>();
        
        // Basic command structure to call a Python function from a module
        command.add(pythonExecutablePath);
        command.add("-c");
        
        // Build the Python code string to import module and call function
        StringBuilder pythonCode = new StringBuilder();
        pythonCode.append("import sys; ")
                 .append("sys.path.append('").append(pythonModulesPath).append("'); ")
                 .append("import ").append(moduleName).append("; ")
                 .append("print(").append(moduleName).append(".").append(functionName).append("(");
        
        // Add function arguments
        for (int i = 0; i < args.length; i++) {
            if (i > 0) {
                pythonCode.append(", ");
            }
            // Escape quotes in the argument
            String escapedArg = args[i].replace("\"", "\\\"");
            pythonCode.append("\"").append(escapedArg).append("\"");
        }
        pythonCode.append("))");
        
        command.add(pythonCode.toString());
        
        // Execute the command
        ProcessBuilder processBuilder = new ProcessBuilder(command);
        Process process = processBuilder.start();
        
        // Read the output
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }
        
        // Check for errors
        BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
        StringBuilder error = new StringBuilder();
        while ((line = errorReader.readLine()) != null) {
            error.append(line).append("\n");
        }
        
        try {
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                throw new IOException("Python process exited with code " + exitCode + ": " + error.toString());
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IOException("Python process was interrupted", e);
        }
        
        return output.toString().trim();
    }
    
    /**
     * Simple method to test if the Python bridge is working
     * 
     * @return A test message if successful
     * @throws IOException If the bridge is not working
     */
    public String testBridge() throws IOException {
        try {
            List<String> command = new ArrayList<>();
            command.add(pythonExecutablePath);
            command.add("-c");
            command.add("print('Python bridge is working!')");
            
            ProcessBuilder processBuilder = new ProcessBuilder(command);
            Process process = processBuilder.start();
            
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line);
            }
            
            process.waitFor();
            return output.toString();
        } catch (Exception e) {
            throw new IOException("Python bridge test failed: " + e.getMessage(), e);
        }
    }
    
    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java -jar pythonbridge.jar <python-path> <modules-path> [module-name] [function-name] [args...]");
            return;
        }
        
        try {
            PythonBridge bridge = new PythonBridge(args[0], args[1]);
            
            if (args.length == 2) {
                // Just test the bridge
                System.out.println(bridge.testBridge());
            } else if (args.length >= 4) {
                // Call a specific function
                String moduleName = args[2];
                String functionName = args[3];
                
                String[] functionArgs = new String[args.length - 4];
                System.arraycopy(args, 4, functionArgs, 0, functionArgs.length);
                
                String result = bridge.callPythonFunction(moduleName, functionName, functionArgs);
                System.out.println(result);
            }
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
