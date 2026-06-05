import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { toast } from "sonner";
import { Copy, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { NewsletterViewer } from "@/components/NewsletterViewer";
import { getLatestNewsletter } from "@/services/api";

export const Route = createFileRoute("/newsletter")({
  head: () => ({
    meta: [
      { title: "Latest Newsletter — The AI Dispatch" },
      { name: "description", content: "Read the latest issue of The AI Dispatch." },
    ],
  }),
  component: NewsletterPage,
});

function NewsletterPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["latest-newsletter"],
    queryFn: getLatestNewsletter,
  });

  const onCopy = async () => {
    if (!data) return;
    await navigator.clipboard.writeText(`${data.title}\n\n${data.content}`);
    toast.success("Newsletter copied to clipboard");
  };

  const onDownload = () => {
    toast.info("PDF download coming soon");
  };

  return (
    <main className="mx-auto max-w-4xl px-4 py-12">
      {isLoading && (
        <div className="space-y-6">
          <Skeleton className="h-8 w-40" />
          <Skeleton className="h-14 w-3/4" />
          <Skeleton className="h-4 w-32" />
          <div className="space-y-3 pt-6">
            {Array.from({ length: 8 }).map((_, i) => (
              <Skeleton key={i} className="h-4 w-full" />
            ))}
          </div>
        </div>
      )}

      {isError && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/10 p-6 text-sm text-destructive">
          Couldn't load the newsletter. Check that the backend is reachable.
        </div>
      )}

      {data && (
        <>
          <div className="mb-8 flex justify-end gap-2">
            <Button variant="outline" size="sm" onClick={onCopy}>
              <Copy className="mr-2 h-4 w-4" /> Copy
            </Button>
            <Button variant="outline" size="sm" onClick={onDownload}>
              <Download className="mr-2 h-4 w-4" /> Download PDF
            </Button>
          </div>
          <NewsletterViewer newsletter={data} />
        </>
      )}
    </main>
  );
}
