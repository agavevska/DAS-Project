package ukim.finki.mk.probnalab.repository.jpa;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import ukim.finki.mk.probnalab.model.Event;

import java.util.List;

@Repository
public interface JpaEventRepository extends JpaRepository<Event, Long> {
    @Query("SELECT e FROM Event e WHERE e.name LIKE %:keyword%")
    List<Event> searchEvents(@Param("keyword") String keyword);

    @Query("SELECT e FROM Event e WHERE e.name LIKE %:keyword% AND e.popularityScore > :value")
    List<Event> searchEventsByTwoParameters(@Param("keyword") String keyword, @Param("value") double value);
}
