import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { Badge } from "@/components/ui/badge";

import { StoryCard } from "@/components/StoryCard";
import { getTopStories } from "@/services/api";
import type { Story } from "@/services/api";

export const Route = createFileRoute("/top-stories")({
  head: () => ({
    meta: [
      { title: "Top Stories — The AI Dispatch" },
      {
        name: "description",
        content: "The most important AI stories, ranked by AI.",
      },
    ],
  }),
  component: TopStoriesPage,
});

function TopStoriesPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["top-stories"],
    queryFn: getTopStories,
  });

  const [q, setQ] = useState("");
  const [source, setSource] = useState<string>("all");
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);

  const sources = useMemo(() => {
    const s = new Set<string>();

    data?.forEach((d) => s.add(d.source));

    return Array.from(s).sort();
  }, [data]);

  const filtered = useMemo(() => {
    if (!data) return [];

    return [...data]
      .filter((s) =>
        source === "all"
          ? true
          : s.source === source
      )
      .filter((s) =>
        q.trim()
          ? (
              s.title +
              " " +
              s.summary
            )
              .toLowerCase()
              .includes(q.toLowerCase())
          : true
      )
      .sort((a, b) => b.score - a.score);
  }, [data, q, source]);

  return (
    <main className="mx-auto max-w-6xl px-4 py-12">
      <header className="mb-8">
        <p className="text-sm font-medium text-muted-foreground">
          Curated by AI
        </p>

        <h1 className="mt-1 text-3xl font-semibold tracking-tight md:text-4xl">
          Top Stories
        </h1>

        <p className="mt-2 max-w-2xl text-muted-foreground">
          The highest-ranked AI stories from the latest pipeline run.
        </p>
      </header>

      <div className="mb-6 flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />

          <Input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Search stories…"
            className="pl-9"
          />
        </div>

        <Select
          value={source}
          onValueChange={setSource}
        >
          <SelectTrigger className="sm:w-[200px]">
            <SelectValue placeholder="All sources" />
          </SelectTrigger>

          <SelectContent>
            <SelectItem value="all">
              All sources
            </SelectItem>

            {sources.map((s) => (
              <SelectItem
                key={s}
                value={s}
              >
                {s}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {isLoading && (
        <div className="grid gap-4 md:grid-cols-2">
          {Array.from({ length: 6 }).map(
            (_, i) => (
              <Skeleton
                key={i}
                className="h-48 w-full"
              />
            )
          )}
        </div>
      )}

      {isError && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-6 text-sm text-destructive">
          Couldn't load stories. Make sure
          the API is running at the configured
          base URL.
        </div>
      )}

      {!isLoading &&
        !isError &&
        filtered.length === 0 && (
          <p className="text-center text-muted-foreground">
            No stories match your filters.
          </p>
        )}

      <div className="grid gap-4 md:grid-cols-2">
        {filtered.map((story) => (
          <div
            key={story.id}
            className="cursor-pointer"
            onClick={() =>
              setSelectedStory(story)
            }
          >
            <StoryCard story={story} />
          </div>
        ))}
      </div>

      <Dialog
        open={!!selectedStory}
        onOpenChange={() =>
          setSelectedStory(null)
        }
      >
        <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-xl leading-relaxed">
              {selectedStory?.title}
            </DialogTitle>
          </DialogHeader>

          <div className="space-y-4">
            <div className="flex gap-2">
              <Badge variant="outline">
                {selectedStory?.source}
              </Badge>

              <Badge>
                Score: {selectedStory?.score}
              </Badge>
            </div>

            <p className="whitespace-pre-wrap leading-relaxed text-muted-foreground">
              {selectedStory?.summary}
            </p>

            {selectedStory?.url && (
              <a
                href={selectedStory.url}
                target="_blank"
                rel="noreferrer"
                className="inline-block font-medium hover:underline"
              >
                Read Original Article →
              </a>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </main>
  );
}