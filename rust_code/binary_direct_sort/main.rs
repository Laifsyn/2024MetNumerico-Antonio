use core::fmt;
use std::{io, vec};

use crossterm::event::{self, Event, KeyCode, KeyEvent, KeyEventKind};
use ratatui::buffer::Buffer;
use ratatui::layout::Rect;
use ratatui::style::{Color, Stylize};
use ratatui::symbols::border;
use ratatui::text::{Line, Text};
use ratatui::widgets::{Block, Paragraph, Widget};
use ratatui::{DefaultTerminal, Frame};
mod binary_search;
fn main() -> io::Result<()> {
    binary_search::main();
    println!("End of the program");
    let mut terminal = ratatui::init();
    let app_result = App::default().run(&mut terminal);
    ratatui::restore();
    app_result
}

#[derive(Debug, Default)]
pub struct App {
    counter: usize,
    exit: bool,
    buff: Vec<ContentAlias>,
    buff_next: Vec<ContentAlias>,
    instructions: Vec<Vec<Line<'static>>>,
}

type ContentAlias = usize;
impl App {
    const WIDTH: usize = "Ordenamiento Anterior: ".len() + 5;

    /// runs the application's main loop until the user quits
    pub fn run(&mut self, terminal: &mut DefaultTerminal) -> io::Result<()> {
        self.populate_instructions();
        while !self.exit {
            terminal.draw(|frame| self.draw(frame))?;
            self.handle_events()?;
        }
        Ok(())
    }

    fn draw(&self, frame: &mut Frame) {
        frame.render_widget(self, frame.area());
    }

    fn handle_key_event(&mut self, key_event: KeyEvent) {
        match key_event.code {
            KeyCode::Char('q') => self.exit(),
            KeyCode::Left => self.decrement_counter(),
            KeyCode::Right => self.increment_counter(),
            KeyCode::Char('r') => {
                // self.counter = 0;

                self.populate_instructions();
            }
            _ => {}
        }
    }

    fn populate_instructions(&mut self) {
        self.instructions.clear();
        use rand::prelude::*;
        let mut rng = rand::thread_rng();
        let vec_size = rng.gen_range(5..20);
        let nums: Vec<ContentAlias> =
            (0..).take(vec_size).map(|_| rng.gen_range(0usize..150)).collect();
        self.buff = nums;
        self.buff_next = self.buff.clone();

        let step_position =
            Line::from(vec!["Paso: ".to_string().into(), self.counter.to_string().yellow()])
                .centered();
        let width = App::WIDTH;
        let indexes = format!("{t:>width$}: {}", format_as_vec_index(&self.buff), t = "Índices");
        let initial_state =
            format!("{t:>width$}: {}", format_vec(&self.buff), t = "Estado Inicial");

        let lines = vec![step_position, indexes.clone().into(), initial_state.clone().into()];
        self.instructions.push(lines);

        use binary_search::BinaryInsertionSort;
        let mut sorter = BinaryInsertionSort::new(&mut self.buff_next);
        let mut idx = 0;
        let clr_not_compare = Color::Rgb(124, 80, 80);
        let clr_compare = Color::Rgb(45, 150, 122);
        while sorter.next().is_some() {
            idx += 1;
            let vec_f = format_vec;
            let e = vec!["Paso: ".to_string().white(), idx.to_string().yellow()];
            let counter: Line<'_> = Line::from(e).alignment(ratatui::layout::Alignment::Center);
            let previous_ordering =
                format!("{t:>width$}: {}", vec_f(&self.buff), t = "Ordenamiento Anterior");
            let cola = self
                .buff
                .get(sorter.sorted_until() - 1)
                .expect("Expects index to be in bounds")
                .clone();
            self.buff = sorter.peek().to_vec();
            let indice_de_paro = { self.buff.iter().take_while(|&x| x < &cola).count() };
            let sorted_state =
                format!("{t:>width$}: {}", format_vec(&self.buff), t = "Después de Ordenar");

            let previous_split = previous_ordering.split(',');
            let last_iteration = previous_split.clone().count() - 1;
            let previous_ordering = previous_split
                .enumerate()
                .map(|(idx, line)| {
                    let mut line = String::from(line);
                    if last_iteration != idx {
                        line.push(',');
                    }
                    // Colorear entre Segmentos procesados, cola de partición y Segmentos no
                    // procesados
                    match idx.cmp(&(sorter.sorted_until() - 1)) {
                        std::cmp::Ordering::Less => {
                            if (idx) < (indice_de_paro) {
                                // Segmentos que no se comparan
                                line.fg(clr_not_compare)
                            } else {
                                // Segmento que sí se compara
                                line.fg(clr_compare)
                            }
                        }
                        std::cmp::Ordering::Equal => line.fg(Color::LightMagenta),
                        std::cmp::Ordering::Greater => line.fg(Color::Cyan),
                    }
                })
                .collect::<Vec<_>>();
            let split = sorted_state.split(',');
            let last_iteration_idx = split.clone().count() - 1;
            let sorted_state = split
                .enumerate()
                .map(|(idx, line)| {
                    let mut line = String::from(line);
                    if last_iteration_idx != idx {
                        line.push(',');
                    }
                    // Colorear entre Segmentos procesados y Segmentos no procesados
                    match (sorter.sorted_until()).cmp(&idx) {
                        std::cmp::Ordering::Greater => line.fg(Color::Cyan),
                        _ => line.fg(Color::Rgb(45, 150, 122)),
                    }
                })
                .collect::<Vec<_>>();

            // Find how to convert a Vec of Styled Content to Line
            let sorted_state = Line::from(sorted_state);
            let lines = vec![
                counter,
                initial_state.clone().into(),
                indexes.clone().into(),
                previous_ordering.into(),
                sorted_state,
                format!(
                    "Índice de paro: {indice_de_paro}, cola: {cola}",
                    indice_de_paro = indice_de_paro
                )
                .into(),
                Line::from(vec![
                    "No se Comparan".fg(clr_not_compare),
                    "  ---  ".white(),
                    "Se Comparan".fg(clr_compare),
                ])
                .centered(),
            ];
            self.instructions.push(lines);
        }
    }

    fn handle_events(&mut self) -> io::Result<()> {
        match event::read()? {
            Event::Key(key_event) if key_event.kind == KeyEventKind::Press => {
                self.handle_key_event(key_event)
            }
            _ => {}
        };
        Ok(())
    }

    fn exit(&mut self) {
        self.exit = true;
    }

    fn increment_counter(&mut self) {
        self.counter = self.counter.saturating_add(1);

        if self.counter >= self.instructions.len() {
            self.counter = self.instructions.len() - 1;
        }
    }

    fn decrement_counter(&mut self) {
        if self.counter > self.instructions.len() {
            self.counter = self.instructions.len() - 1;
        }
        self.counter = self.counter.saturating_sub(1);
    }
}

impl Widget for &App {
    fn render(self, area: Rect, buf: &mut Buffer) {
        let title = Line::from(" Inserción Directa con Búsqueda ".bold());
        let instructions = Line::from(vec![
            " Decrement ".into(),
            "<Left>".blue().bold(),
            " Increment ".into(),
            "<Right>".blue().bold(),
            " Quit ".into(),
            "<Q> ".blue().bold(),
            " New Vec ".into(),
            "<R> ".blue().bold(),
        ]);
        let block = Block::bordered()
            .title(title.centered())
            .title_bottom(instructions.centered())
            .border_set(border::THICK);
        let content_paragraph = Text::from(
            self.instructions
                .get(self.counter)
                .unwrap_or(&self.instructions[self.instructions.len() - 1])
                .clone(),
        );

        Paragraph::new(content_paragraph).centered().block(block).render(area, buf);
    }
}

fn format_vec<T: fmt::Display>(vec: &[T]) -> String {
    let mut formatted = String::new();
    let width = vec.iter().map(|item| (format!("{}", item).len())).max();
    let Some(width) = width else {
        return "[]".to_string();
    };
    formatted.push('[');
    for (i, item) in vec.iter().enumerate() {
        formatted.push_str(&format!("{:<width$}", item));
        if i < vec.len() - 1 {
            formatted.push_str(", ");
        }
    }
    formatted.push(']');
    formatted
}
fn format_as_vec_index<T: fmt::Display>(vec: &[T]) -> String {
    let mut formatted = String::new();
    let width = vec.iter().map(|item| (format!("{}", item).len())).max();
    let Some(width) = width else {
        return "[]".to_string();
    };
    formatted.push('[');
    for (i, _) in vec.iter().enumerate() {
        formatted.push_str(&format!("{:^width$}", i));
        if i < vec.len() - 1 {
            formatted.push_str(", ");
        }
    }
    formatted.push(']');
    formatted
}

mod test {
    #[allow(unused)]
    use super::{format_as_vec_index, format_vec};
    #[test]
    fn test_format_vec() {
        let vec = vec![1, 2, 3, 40, 500];
        assert_eq!(format_vec(&vec), "[  1,   2,   3,  40, 500]");
    }
    #[test]
    fn test_format_as_vec_index() {
        let vec = vec![1, 2, 3, 40, 500];
        assert_eq!(format_as_vec_index(&vec), "[ 0 ,  1 ,  2 ,  3 ,  4 ]");
    }

    #[test]
    fn test_format_vec_and_index_same_width() {
        let vec = vec![1, 2, 3, 40, 500];
        assert_eq!(format_vec(&vec).len(), format_as_vec_index(&vec).len());
    }
}
