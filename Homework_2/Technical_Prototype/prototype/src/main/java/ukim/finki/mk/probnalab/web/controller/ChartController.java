package ukim.finki.mk.probnalab.web.controller;


import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import java.io.*;
import java.util.Base64;
import java.util.Map;

@RestController
@RequestMapping("/chart")
public class ChartController {

    @PostMapping("/generate-chart")
    public ResponseEntity<?> generateChart(@RequestBody Map<String, String> companyData) {
        try {
            // Земете го името на компанијата од JSON објектот
            String companyName = companyData.get("companyName");
            System.out.println("Избрано име на компанијата: " + companyName);

            // Патека до Python скриптата
            String pythonScriptPath = "C://Users//User//DAS-Project//Homework_3//Technical_analysis//TechnicalАnalysis.py";
            String pythonExecutable = "python"; // или python3 ако тоа е патеката

            // Проверка дали патеката до скриптата е валидна
            File scriptFile = new File(pythonScriptPath);
            if (!scriptFile.exists()) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Скриптата не постои на дадената патека.");
            }

            // Покрени го Python процесот
            ProcessBuilder processBuilder = new ProcessBuilder(pythonExecutable, pythonScriptPath, companyName);
            processBuilder.redirectErrorStream(true);  // Слушај и за грешки во стандардниот излез
            Process process = processBuilder.start();

            // Прочитај го стандардниот излез (stdout) на Python процесот
            InputStream inputStream = process.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            String line;
            StringBuilder output = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                output.append(line);  // Логирајте го излезот од скриптата
            }

            // Проверете дали процесот заврши успешно
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Грешка во извршувањето на Python скриптата.");
            }

            // Прочитај ја сликата и конвертирај ја во Base64
            String base64Image = output.toString();
            System.out.println(base64Image);// Тука се претпоставува дека Python скриптата го испишала Base64 кодот

            // Враќање на графикот како Base64 слика
            return ResponseEntity.ok().body(new ChartResponse(base64Image));

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();  // Логирајте ја грешката
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Грешка при генерирање на графикот.");
        }
    }

    static class ChartResponse {
        private String chartData;

        public ChartResponse(String chartData) {
            this.chartData = chartData;
        }

        public String getChartData() {
            return chartData;
        }

        public void setChartData(String chartData) {
            this.chartData = chartData;
        }
    }
}
