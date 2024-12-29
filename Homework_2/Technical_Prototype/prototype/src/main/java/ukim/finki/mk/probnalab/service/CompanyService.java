package ukim.finki.mk.probnalab.service;

import ukim.finki.mk.probnalab.model.Company;

import java.util.List;

public interface CompanyService {

    void addCompanies(List<String> newCompanies);

    List<Company> getAllCompanies();
}