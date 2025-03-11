import java.io.*;
import java.util.*;

public class PythonBridge {
    private String pythonExecutablePath;
    private String pythonModulesPath;
    private static Map<String, String> beliefMemory = new HashMap<>();  // Stores belief updates

    public PythonBridge(String pythonExecutablePath, String pythonModulesPath) {
        this.pythonExecutablePath = pythonExecutablePath;
        this.pythonModulesPath = pythonModulesPath;
    }

    public String callPythonFunction(String moduleName, String functionName, String... args) throws IOException {
        List<String> command = new ArrayList<>();
        command.add(pythonExecutablePath);
        command.add("-c");

        StringBuilder pythonCode = new StringBuilder();
        pythonCode.append("import sys; ")
                 .append("sys.path.append('").append(pythonModulesPath).append("'); ")
                 .append("import ").append(moduleName).append("; ")
                 .append("result = ").append(moduleName).append(".").append(functionName).append("(");

        for (int i = 0; i < args.length; i++) {
            if (i > 0) {
                pythonCode.append(", ");
            }
            String escapedArg = args[i].replace("\"", "\\\"");
            pythonCode.append("\"").append(escapedArg).append("\"");
        }
        pythonCode.append("); print(result)");

        command.add(pythonCode.toString());

        ProcessBuilder processBuilder = new ProcessBuilder(command);
        Process process = processBuilder.start();

        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }

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

        String result = output.toString().trim();

        // 🔥 Store belief updates for later use
        if (moduleName.equals("belief_module")) {  
            beliefMemory.put(functionName, result);
        }

        return result;
    }

    // 🔥 Method to retrieve stored belief updates
    public String getBelief(String key) {
        return beliefMemory.getOrDefault(key, "No data");
    }
}
