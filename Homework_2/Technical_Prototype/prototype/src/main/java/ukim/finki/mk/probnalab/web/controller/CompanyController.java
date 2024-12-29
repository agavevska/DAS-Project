package ukim.finki.mk.probnalab.web.controller;


import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import ukim.finki.mk.probnalab.service.CompanyService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CompanyController {

    private final CompanyService companyService;

    public CompanyController(CompanyService companyService) {
        this.companyService = companyService;
    }

    @PostMapping("/companies")
    public ResponseEntity<String> receiveCompanies(@RequestBody Map<String, List<String>> companiesData) {
        List<String> companies = companiesData.get("companies");

        if (companies == null || companies.isEmpty()) {
            System.out.println("Нема компании.");
        }

        companyService.addCompanies(companies);

        System.out.println("Received companies: " + companies);
        return ResponseEntity.ok("Companies received successfully");
    }
}

