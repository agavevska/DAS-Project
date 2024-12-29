package ukim.finki.mk.probnalab.bootstrap;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;
import ukim.finki.mk.probnalab.model.Event;
import ukim.finki.mk.probnalab.repository.jpa.JpaEventRepository;

import java.util.ArrayList;
import java.util.List;

@Component
public class DataHolder {
    public static List<Event> events=null;

    private final JpaEventRepository eventRepository;

    public DataHolder(JpaEventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    @PostConstruct
    public void init(){
        events=new ArrayList<>();
        events.add(new Event("Photography Workshop", "Learn photography techniques with hands-on practice", 8.0));
        events.add(new Event("Dance Party", "An evening of fun and dancing for all ages", 8.5));
        events.add(new Event("Cooking Class", "Learn to cook delicious meals with expert chefs", 9.0));
        events.add(new Event("Outdoor Movie Night", "Enjoy a film under the stars with friends", 7.5));
        events.add(new Event("Pet Adoption Day", "Find your new furry friend at the local shelter", 7.0));
        events.add(new Event("Game Night", "Join us for board games and snacks", 6.0));
        events.add(new Event("Local Farmers Market", "Shop fresh produce and handmade goods", 8.3));
        events.add(new Event("Book Fair", "A gathering for book lovers and authors.", 6.5));
        events.add(new Event("Coffee Tasting", "Sample different coffee brews from around the world", 9.5));
        events.add(new Event("Nature Walk", "Explore local trails and enjoy the great outdoors", 5.0));
        this.eventRepository.saveAll(events);
    }
}
