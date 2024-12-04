package ukim.finki.mk.probnalab.web.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import ukim.finki.mk.probnalab.service.EventService;

@Controller
@RequestMapping("/events")
public class EventController {

    private final EventService eventService;

    public EventController(EventService eventService) {
        this.eventService = eventService;
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
        model.addAttribute("events", eventService.listAll());
        return "listEvents";
    }

}

