package ukim.finki.mk.probnalab.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
@Entity
public class Event {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String description;
    private double popularityScore;

    public Event(String name, String description, double popularityScore) {
        this.name = name;
        this.description = description;
        this.popularityScore=popularityScore;
    }


    public Event() {
    }
}