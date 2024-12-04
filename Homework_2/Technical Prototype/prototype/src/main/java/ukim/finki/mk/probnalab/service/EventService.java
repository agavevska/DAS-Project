package ukim.finki.mk.probnalab.service;

import ukim.finki.mk.probnalab.model.Event;

import java.util.List;

public interface EventService {
    List<Event> listAll();
    List<Event> searchEvents(String text);

    List<Event> searchEventsByTwoParameters(String text, double value);

}