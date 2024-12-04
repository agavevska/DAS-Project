//package ukim.finki.mk.probnalab.repository.inmem;
//
//
//import org.springframework.stereotype.Repository;
//import ukim.finki.mk.probnalab.bootstrap.DataHolder;
//import ukim.finki.mk.probnalab.model.Event;
//
//import java.util.List;
//
//@Repository
//public class EventRepository {
//
//    public List<Event> findAll(){
//        return DataHolder.events;
//    }
//
//    public List<Event> searchEvents(String text){
//        return DataHolder.events.stream().filter(event -> event.getName().contains(text) || event.getDescription().contains(text)).toList();
//    }
//
//    public List<Event> searchEventsByTwoParameters(String text, double points){
//        return DataHolder.events.stream().filter(event -> (event.getName().contains(text) || event.getDescription().contains(text)) && event.getPopularityScore()>=points).toList();
//    }
//}
