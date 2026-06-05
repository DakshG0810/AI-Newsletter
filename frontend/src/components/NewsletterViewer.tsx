import { lazy, Suspense } from "react";
import { ClientOnly } from "@tanstack/react-router";
import type { Newsletter } from "@/services/api";

const ReactMarkdown = lazy(() =>
  import("react-markdown").then((m) => ({ default: m.default })),
);

export function NewsletterViewer({ newsletter }: { newsletter: Newsletter }) {
  const date = newsletter.published_at ?? newsletter.created_at;
  return (
    <article className="mx-auto max-w-3xl">
      <header className="mb-10 border-b border-border/60 pb-8">
        <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground">
          The AI Dispatch · {
  new Date().toLocaleDateString(
    "en-US",
    {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    }
  )
}
        </p>
        <h1 className="mt-3 text-4xl font-semibold tracking-tight md:text-5xl">{newsletter.title}</h1>
        {date && (
          <p className="mt-3 text-sm text-muted-foreground">
            {new Date(date).toLocaleDateString(undefined, {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </p>
        )}
      </header>

      <div className="prose-newsletter space-y-5 [&_a]:text-foreground [&_a]:underline [&_a]:underline-offset-4 [&_h2]:mt-10 [&_h2]:text-2xl [&_h2]:font-semibold [&_h2]:tracking-tight [&_h3]:mt-8 [&_h3]:text-xl [&_h3]:font-semibold [&_ul]:list-disc [&_ul]:pl-6 [&_ol]:list-decimal [&_ol]:pl-6 [&_blockquote]:border-l-2 [&_blockquote]:border-border [&_blockquote]:pl-4 [&_blockquote]:italic [&_blockquote]:text-muted-foreground [&_code]:rounded [&_code]:bg-muted [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:text-sm">
        <ClientOnly fallback={<p className="whitespace-pre-wrap text-muted-foreground">{newsletter.content}</p>}>
          <Suspense fallback={<p className="text-muted-foreground">Rendering…</p>}>
            <ReactMarkdown>{newsletter.content}</ReactMarkdown>
          </Suspense>
        </ClientOnly>
      </div>
    </article>
  );
}
