package ukim.finki.mk.probnalab.repository.jpa;

import org.springframework.data.jpa.repository.JpaRepository;
import ukim.finki.mk.probnalab.model.Company;

public interface JpaCompanyRepository extends JpaRepository<Company, Long> {
}
