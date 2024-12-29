package ukim.finki.mk.probnalab.service.impl;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ukim.finki.mk.probnalab.model.Company;
import ukim.finki.mk.probnalab.repository.jpa.JpaCompanyRepository;
import ukim.finki.mk.probnalab.service.CompanyService;

import java.util.List;

@Service
public class CompanyServiceImpl implements CompanyService {

    @Autowired
    private JpaCompanyRepository companyRepository;

    @Override
    public void addCompanies(List<String> newCompanies) {
        for (String companyName : newCompanies) {
            Company company = new Company();
            company.setName(companyName);
            companyRepository.save(company); // Запиши во база
        }
    }

    @Override
    public List<Company> getAllCompanies() {
        return companyRepository.findAll();
    }

}
