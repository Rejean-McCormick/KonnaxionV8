// frontend/pages/index.tsx
import React from "react";
import TagsList from "../components/TagsList";

export default function HomePage() {
  return (
    <main>
      <h1>Liste des Expertise Tags</h1>
      <TagsList />
    </main>
  );
}
