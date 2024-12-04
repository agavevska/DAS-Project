package ukim.finki.mk.probnalab.service.impl;

import org.springframework.stereotype.Service;
import ukim.finki.mk.probnalab.model.Event;
import ukim.finki.mk.probnalab.repository.jpa.JpaEventRepository;
import ukim.finki.mk.probnalab.service.EventService;

import java.util.List;

@Service
public class EventServiceImpl implements EventService {
    private final JpaEventRepository eventRepository;

    public EventServiceImpl(JpaEventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }


    @Override
    public List<Event> listAll() {
        return eventRepository.findAll();
    }

    @Override
    public List<Event> searchEvents(String text) {
        return eventRepository.searchEvents(text);
    }

    @Override
    public List<Event> searchEventsByTwoParameters(String text, double value) {
        return eventRepository.searchEventsByTwoParameters(text, value);
    }
}
