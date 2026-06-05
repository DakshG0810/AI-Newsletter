import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { Layers, TrendingUp, Mail, Loader2, RefreshCw, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatCard } from "@/components/StatCard";
import { generateNewsletter, getStats } from "@/services/api";

export const Route = createFileRoute("/dashboard")({
  head: () => ({
    meta: [
      { title: "Dashboard — The AI Dispatch" },
      { name: "description", content: "Monitor your AI news pipeline and generate newsletters." },
    ],
  }),
  component: Dashboard,
});

function Dashboard() {
  const qc = useQueryClient();
  const stats = useQuery({ queryKey: ["stats"], queryFn: getStats });

  const generate = useMutation({
    mutationFn: generateNewsletter,
    onSuccess: () => {
      toast.success("Newsletter generated successfully");
      qc.invalidateQueries({ queryKey: ["stats"] });
      qc.invalidateQueries({ queryKey: ["latest-newsletter"] });
    },
    onError: () => toast.error("Failed to generate newsletter"),
  });

  const refresh = () => {
    qc.invalidateQueries({ queryKey: ["stats"] });
    toast.success("Data refreshed");
  };

  return (
    <main className="mx-auto max-w-6xl px-4 py-12">
      <div className="flex items-end justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">Admin</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight md:text-4xl">Dashboard</h1>
        </div>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        <StatCard label="Total Articles" value={stats.data?.articles} loading={stats.isLoading} icon={Layers} />
        <StatCard label="Top Stories" value={stats.data?.top_stories} loading={stats.isLoading} icon={TrendingUp} />
        <StatCard label="Generated Newsletters" value={stats.data?.newsletters} loading={stats.isLoading} icon={Mail} />
      </div>

      <Card className="mt-8 border-border/60">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl">
            <Sparkles className="h-5 w-5" /> Actions
          </CardTitle>
          <CardDescription>Run pipeline actions on demand.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          <Button onClick={() => generate.mutate()} disabled={generate.isPending}>
            {generate.isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Generating…
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" /> Generate Newsletter
              </>
            )}
          </Button>
          <Button variant="outline" onClick={refresh}>
            <RefreshCw className="mr-2 h-4 w-4" /> Refresh Data
          </Button>
        </CardContent>
      </Card>
    </main>
  );
}
