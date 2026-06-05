import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ExternalLink } from "lucide-react";
import type { Story } from "@/services/api";

function scoreTone(score: number) {
  if (score >= 8) return "bg-accent text-accent-foreground";
  if (score >= 5) return "bg-secondary text-secondary-foreground";
  return "bg-muted text-muted-foreground";
}

export function StoryCard({ story }: { story: Story }) {
  return (
    <Card className="h-[280px] border-border/60 transition-shadow hover:shadow-md">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <a
            href={story.url}
            target="_blank"
            rel="noreferrer"
            className="hover:underline"
          >
            <h3 className="line-clamp-2 text-lg font-semibold leading-snug tracking-tight">
              {story.title}
            </h3>
          </a>

          <Badge className={`shrink-0 ${scoreTone(story.score)}`}>
            {story.score}
          </Badge>
        </div>

        <div className="mt-2">
          <a
            href={story.url}
            target="_blank"
            rel="noreferrer"
          >
            <Badge
              variant="outline"
              className="flex w-fit items-center gap-1 cursor-pointer hover:bg-muted"
            >
              {story.source}
              <ExternalLink className="h-3 w-3" />
            </Badge>
          </a>
        </div>
      </CardHeader>

      <CardContent>
        <p className="line-clamp-5 text-sm leading-relaxed text-muted-foreground">
          {story.summary
            ?.replace(/[#*]/g, "")
            ?.replace(/\n/g, " ")}
        </p>
      </CardContent>
    </Card>
  );
}