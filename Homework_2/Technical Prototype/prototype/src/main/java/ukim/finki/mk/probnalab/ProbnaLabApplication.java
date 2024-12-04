package ukim.finki.mk.probnalab;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.ServletComponentScan;

@SpringBootApplication
@ServletComponentScan
public class ProbnaLabApplication {

    public static void main(String[] args) {
        SpringApplication.run(ProbnaLabApplication.class, args);
    }

}
