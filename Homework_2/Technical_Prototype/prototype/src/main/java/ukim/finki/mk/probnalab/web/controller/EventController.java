package ukim.finki.mk.probnalab.web.controller;


import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import ukim.finki.mk.probnalab.model.Company;
import ukim.finki.mk.probnalab.service.CompanyService;
import ukim.finki.mk.probnalab.service.EventService;

import java.util.List;

@Controller
@RequestMapping("/events")
public class EventController {

    private final EventService eventService;
    private final CompanyService companyService;

    public EventController(EventService eventService, CompanyService companyService) {
        this.eventService = eventService;
        this.companyService = companyService;
    }


    @GetMapping()
    public String getRegisterPage(@RequestParam(required = false) String error, Model model){
        return "register";
    }

    @GetMapping("/login")
    public String getLoginPage(@RequestParam(required = false) String error, Model model){
        return "login";
    }

    @GetMapping("/listEvents")
    public String getEventsPage(@RequestParam(required = false) String error, Model model){
        List<Company> companies = companyService.getAllCompanies();

        model.addAttribute("companies", companies);
        return "home";
    }


    @GetMapping("/analysis")
    public String analysisPage(@RequestParam(required = false) String error, Model model) {
        List<Company> companies = companyService.getAllCompanies();

        model.addAttribute("companies", companies);
        return "analysis";
    }

}

